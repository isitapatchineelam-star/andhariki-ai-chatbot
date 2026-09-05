from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/')
def home():
    return '<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Andhariki AI</title><style>body{font-family:Arial;background:#f0f2f5;margin:0;display:flex;justify-content:center;padding:10px}.box{background:#fff;width:100%;max-width:400px;border-radius:20px;display:flex;flex-direction:column;height:85vh}.head{padding:15px;text-align:center;font-weight:bold;border-bottom:1px solid #eee}#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:8px}.user{background:#0084ff;color:#fff;padding:10px;border-radius:15px;align-self:flex-end}.bot{background:#e4e6eb;padding:10px;border-radius:15px;align-self:flex-start;max-width:85%}.foot{display:flex;gap:8px;padding:12px}input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc}button{padding:12px 18px;border-radius:25px;border:none;background:#0084ff;color:#fff}</style></head><body><div class="box"><div class="head">Andhariki AI - Satya</div><div id="chat"><div class="bot">Hi Satya! Nenu ready! Yee question adugu - Hi avasaram ledu!</div></div><div class="foot"><input id="m" placeholder="Type chey..." onkeypress="if(event.key===\'Enter\')send()"><button onclick="send()">Send</button></div></div><script>async function send(){let i=document.getElementById("m");let v=i.value.trim();if(!v)return;let c=document.getElementById("chat");c.innerHTML+=`<div class=user>${v}</div>`;i.value="";c.scrollTop=c.scrollHeight;let id="a"+Date.now();c.innerHTML+=`<div class=bot id=${id}>Typing...</div>`;try{let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:v})});let d=await r.json();document.getElementById(id).innerText=d.reply}catch(e){document.getElementById(id).innerText="Error"}c.scrollTop=c.scrollHeight;}</script></body></html>'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.get_json().get('message','')
        key = os.environ.get('GEMINI_API_KEY')
        import google.generativeai as genai
        genai.configure(api_key=key)
        for name in ['gemini-1.5-flash','gemini-1.5-flash-latest','gemini-pro','gemini-1.0-pro']:
            try:
                m = genai.GenerativeModel(name)
                r = m.generate_content(msg)
                if r.text: return jsonify({"reply": r.text})
            except: continue
        return jsonify({"reply":"Model busy - malli try chey"})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:200]}"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
