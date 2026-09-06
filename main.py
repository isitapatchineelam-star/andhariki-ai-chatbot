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
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{box-sizing:border-box}
body{margin:0;font-family: -apple-system, BlinkMacSystemFont, sans-serif;background:#0b141a;color:#e9edef;display:flex;flex-direction:column;height:100vh;height:100dvh}
.header{padding:10px 16px;display:flex;align-items:center;gap:12px;background:#202c33;position:sticky;top:0;z-index:10}
.logo{width:40px;height:40px;background:#00a884;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px}
.chat{flex:1;overflow-y:auto;padding:15px 10px;max-width:800px;margin:0 auto;width:100%;background:#0b141a;background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');background-repeat:repeat;opacity:1}
.msg{margin:8px 0;padding:8px 12px;border-radius:12px;max-width:75%;line-height:1.5;word-wrap:break-word;font-size:14.5px;white-space:pre-wrap;box-shadow:0 1px 0.5px rgba(0,0,0,0.13)}
.user{background:#005c4b;color:#e9edef;margin-left:auto;border-top-right-radius:0}
.ai{background:#202c33;color:#e9edef;border-top-left-radius:0}
.msg img{max-width:200px;border-radius:8px;margin-bottom:5px}
.input-area{padding:8px 10px;background:#111b21;position:sticky;bottom:0;display:flex;align-items:flex-end;gap:8px}
.input-box{flex:1;display:flex;gap:4px;background:#2a3942;border-radius:24px;padding:5px 10px;align-items:center;min-height:46px}
.input-box i{color:#8696a0;font-size:22px;cursor:pointer;padding:6px}
.input-box input{flex:1;border:none;background:transparent;outline:none;font-size:15px;padding:8px 4px;color:#fff}
.input-box input::placeholder{color:#8696a0}
.send-btn{background:#00a884;color:#111b21;border:none;width:48px;height:48px;border-radius:50%;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 1px 2px rgba(0,0,0,0.3)}
#fileInput{display:none}
.time{font-size:10px;color:#8696a0;float:right;margin-top:6px;margin-left:10px}
</style>
</head>
<body>
<div class="header"><div class="logo">a</div><div><b>Andhariki AI</b><div style="font-size:12px;color:#8696a0">Voice + ♻️ Scanner</div></div></div>
<div class="chat" id="chat"><div class="msg ai">Hi! Nenu ready! 🎤 Voice tho matladu, 📷 Recycle item ni scan chey! ♻️ <span class="time">now</span></div></div>

<div class="input-area">
  <div class="input-box">
    <i class="fa-regular fa-face-smile" onclick="alert('Emoji keyboard open chey')"></i>
    <input id="inp" placeholder="Message" autocomplete="off" oninput="toggleBtn()">
    <i class="fa-solid fa-paperclip" onclick="document.getElementById('fileInput').click()"></i>
    <i class="fa-solid fa-camera" onclick="document.getElementById('fileInput').click()"></i>
    <input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
  </div>
  <button class="send-btn" id="mainBtn" onclick="handleMain()"><i class="fa-solid fa-microphone" id="mainIcon"></i></button>
</div>

<script>
const chat=document.getElementById('chat'); const inp=document.getElementById('inp');
let recognition; let isListening=false;

function toggleBtn(){
 let icon=document.getElementById('mainIcon');
 if(inp.value.trim().length>0){ icon.className='fa-solid fa-paper-plane'; }
 else { icon.className='fa-solid fa-microphone'; }
}
function handleMain(){
 if(inp.value.trim().length>0){ send(); } else { startVoice(); }
}
function startVoice(){
 if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){ alert('Voice ki Chrome browser vadandi'); return; }
 const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
 recognition = new SR(); recognition.lang='te-IN'; recognition.interimResults=false;
 recognition.onstart=()=>{ document.getElementById('mainIcon').className='fa-solid fa-stop'; isListening=true; };
 recognition.onresult=(e)=>{ inp.value=e.results[0][0].transcript; toggleBtn(); send(); };
 recognition.onend=()=>{ document.getElementById('mainIcon').className='fa-solid fa-microphone'; isListening=false; };
 recognition.start();
}
inp.addEventListener('keypress',e=>{ if(e.key==='Enter') send(); });

async function send(){
 let t=inp.value.trim(); if(!t) return;
 let time=new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
 chat.innerHTML+=`<div class="msg user">${t}<span class="time">${time} ✓✓</span></div>`;
 inp.value=''; toggleBtn(); chat.scrollTop=chat.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  let time2=new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  chat.innerHTML+=`<div class="msg ai">${d.reply}<span class="time">${time2}</span></div>`;
 }catch(e){ chat.innerHTML+=`<div class="msg ai">Network error, malli try chey</div>` }
 chat.scrollTop=chat.scrollHeight;
}

async function scanImage(event){
 let file=event.target.files[0]; if(!file) return;
 let reader=new FileReader();
 reader.onload=async function(){
  let base64=reader.result.split(',')[1];
  let time=new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  chat.innerHTML+=`<div class="msg user"><img src="${reader.result}"><br>♻️ Scanning...<span class="time">${time} ✓✓</span></div>`;
  chat.scrollTop=chat.scrollHeight;
  let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:base64})});
  let d=await r.json();
  let time2=new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  chat.innerHTML+=`<div class="msg ai">♻️ <b>Scanner:</b><br>${d.reply}<span class="time">${time2}</span></div>`;
  chat.scrollTop=chat.scrollHeight;
 }
 reader.readAsDataURL(file);
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
    if GROQ_API_KEY:
        for model in ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]:
            try:
                res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json={"model": model,"messages": [{"role":"system","content":"You are Andhariki AI, friendly. Reply in user's language."},{"role":"user","content":user_msg}],"temperature":0.7,"max_tokens":1024},timeout=25)
                data=res.json()
                if "choices" in data: return jsonify({"reply": data["choices"][0]["message"]["content"]})
            except: continue
    if GEMINI_API_KEY:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            res=requests.post(url,json={"contents":[{"parts":[{"text":user_msg}]}]},timeout=25)
            data=res.json()
            if "candidates" in data: return jsonify({"reply": data["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass
    return jsonify({"reply":"Konchem busy, malli adugu"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img_data = request.json.get("image","")
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload={"contents":[{"parts":[{"text":"You are recycling scanner. Analyze image, tell: 1) What item? 2) Recyclable or not? 3) Which bin? Blue/Green/Red? 4) How to recycle? Short answer Telugu+English mix, emojis."},{"inline_data":{"mime_type":"image/jpeg","data":img_data}}]}]}
        res=requests.post(url,json=payload,timeout=30)
        data=res.json()
        text=data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply":text})
    except Exception as e:
        return jsonify({"reply":"Clear photo pettu, malli try chey"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
