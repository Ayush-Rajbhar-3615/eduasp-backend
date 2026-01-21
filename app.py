import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so your Netlify frontend can talk to this server
CORS(app)

# --- CONFIGURATION ---
# We get the API Key securely from Railway's settings
GOOGLE_API_KEY = os.environ.get("AIzaSyB-FTHm7XzXAqfLclc4v9u6kGe5PLTcLpk")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/')
def home():
    return "eduASP Backend is Live and Running!"

@app.route('/ask', methods=['POST'])
def ask_gemini():
    # Security Check
    if not GOOGLE_API_KEY:
        return jsonify({"error": "API Key is missing on Server"}), 500

    try:
        data = request.json
        grade = data.get('grade')
        subject = data.get('subject')
        question = data.get('question')

        print(f"Received question: {question}") # Log for debugging

        # The AI Prompt
        prompt = f"""
        Act as a friendly tutor for a Class {grade} student studying {subject}.
        Question: "{question}"
        
        Instructions:
        1. Explain the answer simply.
        2. Use bullet points for readability.
        3. highlight key terms in **bold**.
        4. Keep it under 200 words.
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return jsonify({"answer": response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Railway requires us to listen on a specific PORT they provide
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)