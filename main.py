import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(_name_)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get('message','').strip() if data else ''
        if not user_msg:
            return jsonify({"reply": "Emaina type cheyyi bro!"})
        if not API_KEY:
            return jsonify({"reply": "Server lo API Key ledu - Render Environment lo GEMINI_API_KEY pettali"})
        
        prompt = f"You are Andhariki AI, friendly Telugu+English assistant. Reply in user's language: {user_msg}"
        res = model.generate_content(prompt)
        return jsonify({"reply": res.text})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": f"Error vachindi: {str(e)[:150]}"})

@app.route('/health')
def health():
    return jsonify({"status":"ok"})

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
