from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Andhariki AI</title>
<style>
body { margin:0; font-family: 'Google Sans', sans-serif; background: #131314; color: #e3; display:flex; flex-direction:column; height:100vh; }
.header { padding: 15px 20px; display:flex; align-items:center; gap:10px; border-bottom: 1px solid #2d2e30; }
.logo { width:32px; height:32px; background: linear-gradient(135deg, #8ab4f8, #aecbfa); border-radius:50%; display:flex; align-items:center; justify-content:center; color:#202124; font-weight:bold; }
.chat { flex:1; overflow-y:auto; padding:20px; max-width:800px; margin:0 auto; width:100%; box-sizing:border-box; }
.msg { margin:15px 0; padding:12px 16px; border-radius:18px; max-width:80%; line-height:1.5; }
.user { background:#2d2e30; margin-left:auto; border-bottom-right-radius:4px; }
.ai { background: transparent; }
.input-box { max-width:800px; margin:0 auto 20px; width:90%; background:#1e1f20; border-radius:25px; display:flex; padding:8px; border:1px solid #333; }
.input-box input { flex:1; background:transparent; border:none; color:white; padding:10px 15px; outline:none; font-size:16px; }
.input-box button { background:white; border:none; width:40px; height:40px; border-radius:50%; cursor:pointer; font-size:18px; }
</style>
</head>
<body>
<div class="header"><div class="logo">a</div><div><b>Andhariki</b><div style="font-size:12px; color:#9aa0a6;">Ask anything - English, తెలుగు, हिन्दी & more</div></div></div>
<div class="chat" id="chat">
<div class="msg ai">Hi Satya! Nenu ready! Yemi adagalo adugu 😊</div>
</div>
<div class="input-box">
<input id="inp" placeholder="Type your message" onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">➤</button>
</div>
<script>
async function send(){
let i=document.getElementById('inp'); let t=i.value.trim(); if(!t)return;
let c=document.getElementById('chat');
c.innerHTML+=`<div class="msg user">${t}</div>`; i.value='';
c.scrollTop=c.scrollHeight;
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
let d=await r.json();
c.innerHTML+=`<div class="msg ai">${d.reply}</div>`;
c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    if not GROQ_API_KEY:
        return jsonify({"reply": "Render lo GROQ_API_KEY ledu! Environment lo pettu Satya"})

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are Andhariki AI, friendly Telugu assistant. Reply in user's language. User name is Satya."},
                    {"role": "user", "content": user_msg}
                ]
            },
            timeout=20
        )
        data = res.json()
        if "choices" in data:
            return jsonify({"reply": data["choices"][0]["message"]["content"]})
        else:
            return jsonify({"reply": f"Groq Error: {data}"})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
