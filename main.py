# app.py
from flask import Flask, request, jsonify, send_from_directory
import requests
import re
import time

app = Flask(__name__, static_folder='templates')

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def filter_thinking(response):
    # Remove content between <think> tags
    cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    # Clean up any extra whitespace
    cleaned_response = cleaned_response.strip()
    return cleaned_response

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'home.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Construct the prompt
    prompt = f"{user_message}"
    
    # Call Ollama API
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        # Get the response and filter out thinking content
        response_text = response.json().get('response', '')
        filtered_response = filter_thinking(response_text)
        
        return jsonify({
            'response': filtered_response,
            'timestamp': time.strftime('%H:%M')
        })
    else:
        return jsonify({
            'error': 'Failed to get response from model',
            'timestamp': time.strftime('%H:%M')
        }), 500

if __name__ == '__main__':
    app.run(debug=True)