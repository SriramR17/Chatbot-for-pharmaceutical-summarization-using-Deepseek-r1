# Pharmaceutical Literature Summarization Chatbot

## Overview
This project is a conversational chatbot designed to summarize pharmaceutical literature and text using DeepSeek-R1 8B. The chatbot is built with a Flask backend and an HTML, CSS, and JavaScript frontend. The model runs locally using Ollama, enabling efficient and private summarization of medical and pharmaceutical texts.

## Features
- **Summarization of Pharmaceutical Texts**: Provides concise and accurate summaries of pharmaceutical literature.
- **Conversational Interface**: Users can interact with the chatbot in a natural conversational manner.
- **Locally Hosted**: No reliance on external APIs; all processing happens locally for privacy and efficiency.
- **History Storage**: Chat history is stored in MySQL for future reference.

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- **Ollama** (for running DeepSeek-R1 8B locally)
- **Python 3.8+**
- **Flask**
- **MySQL Connector Python**
- **Node.js** (for frontend dependencies if needed)

### Step 1: Install and Set Up Ollama
1. Download and install [Ollama](https://ollama.com) based on your OS.
2. Open a terminal and verify installation:
   ```sh
   ollama --version
   ```
3. Download the DeepSeek-R1 8B model:
   ```sh
   ollama pull deepseek-r1:8b
   ```

### Step 2: Set Up the Backend
1. Clone this repository:
   ```sh
   git clone https://github.com/SriramR17/Chatbot-for-pharmaceutical-summarization-using-Deepseek-r1.git
   cd pharma-chatbot
   ```
2. **Using Virtual Environment (venv)**:
   - Create a virtual environment and activate it:
     ```sh
     python -m venv venv
     source venv/bin/activate   # On Windows use: venv\Scripts\activate
     ```

3. **Using Conda Environment**:
   - Create and activate a Conda environment:
     ```sh
     conda create --name pharma-chatbot python=3.8
     conda activate pharma-chatbot
     ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run the Flask server:
   ```sh
   python app.py
   ```

### Step 3: Set Up the Frontend
1. Open the `home.html` file in a browser.
2. Ensure the Flask server is running for proper API interaction.

## Future Enhancements
- **Speech Typing**: Enable voice-to-text input for easier interaction.
- **Export Summarized Text**: Allow users to download summaries as PDF or Word documents.
- **Image/Document Upload**: Users will be able to upload images or documents, and the chatbot will extract and summarize content from them.

## Contributions
Feel free to fork this project, submit issues, or create pull requests to improve its functionality.

## License
This project is open-source under the MIT License.

---
Happy Summarizing! 🚀

