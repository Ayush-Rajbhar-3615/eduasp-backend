import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ===============================
# CONFIGURATION
# ===============================
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is missing in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# ===============================
# ROUTES
# ===============================
@app.route("/")
def home():
    return "eduASP Backend is Live and Running!"

@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        grade = data.get("grade")
        subject = data.get("subject")
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        prompt = f"""
Act as a friendly tutor for a Class {grade} student studying {subject}.

Question:
"{question}"

Instructions:
1. Explain simply.
2. Use bullet points.
3. Highlight key terms in **bold**.
4. Keep under 200 words.
"""

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        answer = response.text if response.text else "No response generated."

        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)