from flask import Flask, request, jsonify
import os
app = Flask(__name__)
@app.route('/')
def home():
    return open('index.html').read() if os.path.exists('index.html') else '<h1>Andhariki AI Running</h1>'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        import requests
        msg = request.get_json().get('message','')
        key = os.environ.get('GROQ_API_KEY','').strip()
        if not key:
            return jsonify({"reply":"❌ GROQ_API_KEY ledu Render lo! console.groq.com nundi key pettu"})
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"},
            json={"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":msg}]}, timeout=20)
        data = r.json()
        return jsonify({"reply": data['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:400]}"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
