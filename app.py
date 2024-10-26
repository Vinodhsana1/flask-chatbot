from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import logging

# Load the Google API key from environment variables
GOOGLE_API_KEY = "AIzaSyBbVbqznClXNK3Wx7weqNXSS_Sb4-QT6fE"
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing. Please set it as an environment variable.")

# Configure Generative AI API with the key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)

# Set up error logging
app.logger.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    if len(user_input) > 500:
        return jsonify({"error": "Message too long. Limit to 500 characters."}), 400

    try:
        response_raw = chat.send_message(user_input)
        response = response_raw.text
        return jsonify({"response": response})

    except Exception as e:
        app.logger.error(f"Error during chat processing: {e}")
        return jsonify({"error": "An error occurred while processing your message."}), 500

if __name__ == '__main__':
    app.run(debug=True)
