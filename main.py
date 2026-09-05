import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

app = Flask(_name_)

# Get API Key from Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are Andhariki - a thoughtful, multilingual assistant for everyone.
You can speak English, Telugu (both formal and casual), Hindi, and Hinglish.
Be helpful, friendly, and concise. Always respond in the same language the user used.
If user speaks Telugu, reply in Telugu. If English, reply in English.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"reply": "Please type something!"})

        if not GEMINI_API_KEY:
            return jsonify({"reply": "API Key is missing on server. Please set GEMINI_API_KEY in Render."})

        response = model.generate_content(SYSTEM_PROMPT + "\n\nUser: " + user_message)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Sorry, I couldn't generate a reply. Try again!"})

    except Exception as e:
        print(f"Error: {e}")
        # IMPORTANT: Always return JSON, not HTML
        return jsonify({"reply": f"Sorry, server error: {str(e)[:100]}. Please try again."}), 200

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
