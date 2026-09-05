from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;padding:15px;margin:0}.box{background:#fff;width:100%;max-width:400px;border-radius:20px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,.1)}#chat{height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:8px;margin:12px 0}.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px;align-self:flex-end;max-width:80%}.bot{background:#e4e6eb;color:#000;padding:10px 14px;border-radius:18px;align-self:flex-start;max-width:80%}input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc}button{padding:12px 18px;border-radius:25px;border:none;background:#0084ff;color:#fff;font-weight:bold}.row{display:flex;gap:8px}</style></head><body><div class="box"><h3 style="text-align:center">Andhariki AI 🤖</h3><div id="chat"><div class="bot">Hi Satya! Nenu ready! Adugu 😊</div></div><div class="row"><input id="m" placeholder="Type chey..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div></div><script>async function send(){let i=document.getElementById('m');let v=i.value.trim();if(!v)return;let c=document.getElementById('chat');c.innerHTML+=`<div class=user>${v}</div>`;i.value='';c.scrollTop=c.scrollHeight;let id='t'+Date.now();c.innerHTML+=`<div class=bot id=${id}>Typing...</div>`;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let d=await r.json();document.getElementById(id).innerText=d.reply;c.scrollTop=c.scrollHeight}</script></body></html>"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.json.get('message','')
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({"reply":"API Key ledu! Render -> Environment lo GEMINI_API_KEY add chey Satya"})
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(msg)
        return jsonify({"reply": res.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:200]} - Key check chey"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
