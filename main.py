from flask import Flask, request, jsonify
import os

app = Flask(_name_)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Andhariki AI</title>
<style>
body{font-family:sans-serif;background:#f0f2f5;margin:0;display:flex;justify-content:center;padding:10px}
.box{background:#fff;width:100%;max-width:420px;border-radius:20px;box-shadow:0 4px 15px rgba(0,0,0,.1);display:flex;flex-direction:column;height:90vh}
.head{padding:15px;text-align:center;font-weight:bold;font-size:18px;border-bottom:1px solid #eee}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:8px}
.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px 18px 0 18px;align-self:flex-end;max-width:80%}
.bot{background:#e4e6eb;color:#000;padding:10px 14px;border-radius:18px 18px 18px 0;align-self:flex-start;max-width:85%;white-space:pre-wrap}
.foot{display:flex;gap:8px;padding:12px;border-top:1px solid #eee}
input{flex:1;padding:12px 15px;border-radius:25px;border:1px solid #ccc;outline:none}
button{padding:12px 20px;border-radius:25px;border:none;background:#0084ff;color:#fff;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<div class="box">
<div class="head">Andhariki AI 🤖 - Satya</div>
<div id="chat"><div class="bot">Hi Satya! Nenu ready! Em adagali? 😊 Phone lo kuda ready!</div></div>
<div class="foot"><input id="m" placeholder="Type chey..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div>
</div>
<script>
async function send(){
 let i=document.getElementById('m'); let v=i.value.trim(); if(!v) return;
 let c=document.getElementById('chat'); c.innerHTML+=<div class=user>${v}</div>; i.value=''; c.scrollTop=c.scrollHeight;
 let id='a'+Date.now(); c.innerHTML+=<div class=bot id=${id}>Typing...</div>; c.scrollTop=c.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});
  let d=await r.json();
  document.getElementById(id).innerText=d.reply;
 }catch(e){document.getElementById(id).innerText="Error: "+e.message}
 c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        msg = data.get('message','').strip()
        if not msg:
            return jsonify({"reply": "Message ledu!"})

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({"reply": "❌ GEMINI_API_KEY ledu! Render > Environment lo key pettu!"})

        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # KOTTA MODELS - 404 error fix
        models = ['gemini-2.0-flash', 'gemini-1.5-flash-latest', 'gemini-1.5-flash-001', 'gemini-pro']
        last_err = ""
        for m_name in models:
            try:
                model = genai.GenerativeModel(m_name)
                resp = model.generate_content(msg)
                if resp and resp.text:
                    return jsonify({"reply": resp.text})
            except Exception as e:
                last_err = str(e)
                continue
        
        return jsonify({"reply": f"Gemini Error: {last_err[:300]}"})
    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)[:300]}"})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
