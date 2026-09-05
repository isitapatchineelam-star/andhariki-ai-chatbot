from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Andhariki AI</title>
<style>
body{margin:0;font-family:Arial;background:#f8f9f4;display:flex;justify-content:center}
.box{width:100%;max-width:420px;background:#f8f9f4;height:100vh;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;padding:15px;background:#fff;border-bottom:1px solid #e0e0e0}
.left{display:flex;gap:10px;align-items:center}
.logo{width:45px;height:45px;background:#2d4a3e;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;font-weight:bold}
.title{font-weight:bold;font-size:17px}.sub{font-size:12px;color:#666}
.newchat{color:#2d4a3e;font-size:14px;text-decoration:underline;cursor:pointer}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:12px}
.a-msg{display:flex;gap:8px}
.a-icon{width:32px;height:32px;background:#2d4a3e;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px}
.bubble{padding:12px 14px;border-radius:18px;max-width:78%;font-size:15px;line-height:1.4;white-space:pre-wrap}
.a-bubble{background:#e8ece3;color:#333;border-radius:18px 18px 18px 4px}
.u-bubble{background:#dbe8d3;color:#222;align-self:flex-end;border-radius:18px 18px 4px 18px;margin-left:auto}
.foot{padding:12px;background:#f8f9f4}
.inputbox{display:flex;background:#fff;border:1px solid #ddd;border-radius:25px;padding:6px;align-items:center}
input{flex:1;border:none;outline:none;padding:8px}
.send{width:40px;height:40px;background:#2d4a3e;border:none;border-radius:50%;color:#fff;cursor:pointer;font-size:18px}
</style></head>
<body><div class="box">
<div class="top"><div class="left"><div class="logo">a</div><div><div class="title">Andhariki</div><div class="sub">Ask anything · English, తెలుగు, हिन्दी & more</div></div></div><div class="newchat" onclick="location.reload()">New chat</div></div>
<div id="chat"><div class="a-msg"><div class="a-icon">a</div><div class="bubble a-bubble">Hi Satya! Nenu ready! Yemi adagalo adugu 😊</div></div></div>
<div class="foot"><div class="inputbox"><input id="m" placeholder="Type your message..." onkeypress="if(event.key==='Enter')send()"><button class="send" onclick="send()">➤</button></div></div>
</div>
<script>
async function send(){
 let i=document.getElementById("m");let v=i.value.trim();if(!v)return;
 let c=document.getElementById("chat");c.innerHTML+=`<div class="bubble u-bubble">${v}</div>`;i.value="";c.scrollTop=c.scrollHeight;
 let id="a"+Date.now();c.innerHTML+=`<div class="a-msg"><div class="a-icon">a</div><div class="bubble a-bubble" id="${id}">Typing... ✍️</div></div>`;
 c.scrollTop=c.scrollHeight;
 try{
  let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:v})});
  let d=await r.json();document.getElementById(id).innerText=d.reply
 }catch(e){document.getElementById(id).innerText="Error: "+e}
 c.scrollTop=c.scrollHeight;
}
</script></body></html>
'''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.get_json().get('message','')
        key = os.environ.get('GROQ_API_KEY','').strip()
        if not key:
            return jsonify({"reply": "Render lo GROQ_API_KEY ledu! Environment lo pettu Satya"})

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": f"You are Andhariki AI made by Satya. Reply in same language user uses (Telugu/English/Hindi). Be friendly. User says: {msg}"}]
            }, timeout=30)

        data = r.json()
        if 'choices' in data:
            return jsonify({"reply": data['choices'][0]['message']['content']})
        else:
            return jsonify({"reply": f"Groq Error: {str(data)[:300]}"})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:300]}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
