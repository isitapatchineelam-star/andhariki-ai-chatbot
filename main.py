import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(_name_)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        msg = data.get('message','').strip() if data else ''
        if not msg:
            return jsonify({"reply":"Emaina message pettu bro"})
        if not model:
            return jsonify({"reply":"API Key ledu"})
        res = model.generate_content(f"You are Andhariki AI: {msg}")
        return jsonify({"reply": res.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:150]}"})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
