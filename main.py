from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Andhariki AI</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000;display:flex;flex-direction:column;height:100vh;height:100dvh}
.header{padding:12px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #e5e7eb;background:#fff;position:sticky;top:0;z-index:10}
.logo{width:36px;height:36px;background:#000;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:12px 0;padding:12px 16px;border-radius:20px;max-width:85%;line-height:1.6;word-wrap:break-word;font-size:15px;white-space:pre-wrap}
.user{background:#f0f0f0;margin-left:auto;border-bottom-right-radius:5px}
.ai{background:#f9f9f9;border:1px solid #eee}
.input-area{padding:12px 16px;border-top:1px solid #eee;background:#fff;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;display:flex;gap:10px;background:#f3f4f6;border-radius:28px;padding:6px 6px 6px 18px;align-items:center}
.input-box input{flex:1;border:none;background:transparent;outline:none;font-size:16px;padding:8px 0}
.input-box button{background:#000;color:#fff;border:none;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center}
</style>
</head>
<body>
<div class="header"><div class="logo">a</div><div><b>Andhariki AI</b><div style="font-size:12px;color:#666">Ask anything - English, తెలుగు, हिंदी</div></div></div>
<div class="chat" id="chat"><div class="msg ai">Hi! Nenu ready! Yemi adagalo adugu 😊</div></div>
<div class="input-area"><div class="input-box"><input id="inp" placeholder="Type your message" autocomplete="off"><button onclick="send()">↑</button></div></div>
<script>
const chat=document.getElementById('chat'); const inp=document.getElementById('inp');
inp.addEventListener('keypress',e=>{if(e.key==='Enter')send()});
async function send(){
 let t=inp.value.trim(); if(!t)return;
 chat.innerHTML+=`<div class="msg user">${t}</div>`; inp.value=''; chat.scrollTop=chat.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  chat.innerHTML+=`<div class="msg ai">${d.reply}</div>`;
 }catch(e){ chat.innerHTML+=`<div class="msg ai">Network error, malli try chey</div>` }
 chat.scrollTop=chat.scrollHeight;
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
    user_msg = request.json.get("message","")

    # 1. TRY GROQ
    if GROQ_API_KEY:
        for model in ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]:
            try:
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are Andhariki AI, friendly helpful assistant. Reply in same language user uses - Telugu, English, Hindi. Be helpful, short."},
                            {"role": "user", "content": user_msg}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1024
                    },
                    timeout=25
                )
                data = res.json()
                if "choices" in data and data["choices"]:
                    return jsonify({"reply": data["choices"][0]["message"]["content"]})
            except:
                continue

    # 2. TRY GEMINI BACKUP
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": user_msg}]}]}, timeout=25)
            data = res.json()
            if "candidates" in data:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"reply": text})
        except:
            pass

    return jsonify({"reply": "Konchem busy ga unna, 1 min taruvata malli adugu!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
