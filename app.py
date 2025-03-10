from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import re
import time
import json
import os
import html

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "pharma"

def filter_thinking(response):
    # Remove content between <think> tags
    cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    # Clean up any extra whitespace
    cleaned_response = cleaned_response.strip()
    return cleaned_response

def format_response(response):
    # Remove markdown bold indicators (**)
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
    
    # Ensure sections have proper paragraph breaks
    # Find section titles (capitalized word followed by colon)
    sections = re.split(r'([A-Z][a-zA-Z\s]+:)', cleaned)
    
    formatted_text = ""
    # Skip the first element if it's empty
    start_idx = 0 if sections[0].strip() else 1
    
    # Build formatted text with proper section breaks
    for i in range(start_idx, len(sections)):
        section = sections[i].strip()
        if i % 2 == start_idx % 2:  # It's a section title
            if formatted_text:  # Add extra line break before new sections except the first
                formatted_text += "\n\n"
            formatted_text += section + "\n"
        else:  # It's section content
            # Format list items
            lines = section.split('\n')
            formatted_lines = []
            
            for line in lines:
                # Convert numbered items to bullet points
                line = re.sub(r'^\s*\d+\.\s+', '• ', line)
                # Make sure existing bullet points have proper formatting
                line = re.sub(r'^\s*[•\-*]\s+', '• ', line)
                formatted_lines.append(line)
            
            # Join the lines with proper spacing
            section_content = '\n'.join(formatted_lines)
            # Add paragraph breaks between bullet points
            section_content = re.sub(r'(• [^\n]+)', r'\1\n', section_content)
            formatted_text += section_content
    
    # Remove redundant newlines
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    
    # Convert plain text formatting to HTML for proper display in chat
    html_formatted = formatted_text.replace('\n\n', '<br><br>').replace('\n', '<br>')
    
    # Make section titles bold
    html_formatted = re.sub(r'([A-Z][a-zA-Z\s]+:)<br>', r'<strong>\1</strong><br>', html_formatted)
    
    # Make bullet points more visible
    html_formatted = html_formatted.replace('• ', '<span style="margin-left: 1em">•</span> ')
    
    return html_formatted

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
       
        # Construct the prompt with pharmaceutical context
        prompt = f'''As a pharmaceutical summarizer, analyze and summarize the following text:
       
{user_message}

Provide a clear, concise summary highlighting key points, information, interactions, and important details. 
Format your response with clear section headings and use short paragraphs with proper spacing.
Use this structure:
1. Brief introduction
2. What is [Drug/Topic]?
3. Key Points (with bullet points)
4. Information (with bullet points)
5. Interactions (with bullet points)
6. Important Details (with bullet points)
7. Brief conclusion if needed

Use proper paragraph breaks between sections.'''
       
        # Call Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=30  # Add timeout
        )
       
        if response.status_code == 200:
            # Get the response and filter out thinking content
            response_text = response.json().get('response', '')
            filtered_response = filter_thinking(response_text)
            # Apply additional formatting to generate HTML-formatted text
            formatted_response = format_response(filtered_response)
           
            return jsonify({
                'response': formatted_response,
                'is_html': True,  # Flag to indicate HTML content
                'timestamp': time.strftime('%H:%M')
            })
        else:
            return jsonify({
                'error': f'API Error: {response.status_code}',
                'response': 'I encountered an error processing your request. Please try again.',
                'timestamp': time.strftime('%H:%M')
            }), 500
           
    except requests.exceptions.RequestException as e:
        # Handle connection errors to Ollama
        return jsonify({
            'error': f'Connection error: {str(e)}',
            'response': 'Unable to connect to the AI service. Is Ollama running?',
            'timestamp': time.strftime('%H:%M')
        }), 503
       
    except Exception as e:
        # General error handling
        return jsonify({
            'error': f'Server error: {str(e)}',
            'response': 'An unexpected error occurred. Please try again later.',
            'timestamp': time.strftime('%H:%M')
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Endpoint to get available models (could be expanded in the future)"""
    try:
        return jsonify({
            'current_model': MODEL_NAME,
            'available_models': [MODEL_NAME]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
   
    app.run(debug=True, host='0.0.0.0', port=5000)