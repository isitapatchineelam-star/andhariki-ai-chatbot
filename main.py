from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/')
def home():
    html = '<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Andhariki AI</title><style>body{font-family:Arial;background:#f0f2f5;margin:0;display:flex;justify-content:center;padding:10px}.box{background:#fff;width:100%;max-width:400px;border-radius:20px;box-shadow:0 4px 12px rgba(0,0,0,.1);display:flex;flex-direction:column;height:85vh}.head{padding:15px;text-align:center;font-weight:bold;border-bottom:1px solid #eee}#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:8px}.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px;align-self:flex-end;max-width:80%}.bot{background:#e4e6eb;color:#000;padding:10px 14px;border-radius:18px;align-self:flex-start;max-width:85%}.foot{display:flex;gap:8px;padding:12px;border-top:1px solid #eee}input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc}button{padding:12px 18px;border-radius:25px;border:none;background:#0084ff;color:#fff;font-weight:bold}</style></head><body><div class="box"><div class="head">Andhariki AI - Satya</div><div id="chat"><div class="bot">Hi Satya! Ready! Phone lo kuda ready!</div></div><div class="foot"><input id="m" placeholder="Type chey..." onkeypress="if(event.key===\'Enter\')send()"><button onclick="send()">Send</button></div></div><script>async function send(){let i=document.getElementById("m");let v=i.value.trim();if(!v)return;let c=document.getElementById("chat");c.innerHTML+=`<div class=user>${v}</div>`;i.value="";c.scrollTop=c.scrollHeight;let id="a"+Date.now();c.innerHTML+=`<div class=bot id=${id}>Typing...</div>`;c.scrollTop=c.scrollHeight;try{let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:v})});let d=await r.json();document.getElementById(id).innerText=d.reply}catch(e){document.getElementById(id).innerText="Error:"+e.message}c.scrollTop=c.scrollHeight;}</script></body></html>'
    return html

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.get_json().get('message','')
        key = os.environ.get('GEMINI_API_KEY')
        if not key:
            return jsonify({"reply":"Key ledu Render lo!"})
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        res = model.generate_content(msg)
        return jsonify({"reply":res.text})
    except Exception as e:
        return jsonify({"reply":"Error: "+str(e)[:200]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
