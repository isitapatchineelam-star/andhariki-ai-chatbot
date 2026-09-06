from flask import Flask, request, jsonify
import os, requests, base64

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
.header{padding:12px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #e5e7eb;background:#fff;position:sticky;top:0;z-index:10;justify-content:space-between}
.logo{width:36px;height:36px;background:#000;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:12px 0;padding:12px 16px;border-radius:20px;max-width:85%;line-height:1.6;word-wrap:break-word;font-size:15px;white-space:pre-wrap;position:relative}
.user{background:#f0f0f0;margin-left:auto;border-bottom-right-radius:5px}
.ai{background:#f9f9f9;border:1px solid #eee}
.input-area{padding:12px 16px;border-top:1px solid #eee;background:#fff;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;display:flex;gap:8px;background:#f3f4f6;border-radius:28px;padding:6px 6px 6px 12px;align-items:center}
.input-box input{flex:1;border:none;background:transparent;outline:none;font-size:16px;padding:8px 0}
.icon-btn{background:#fff;border:1px solid #ddd;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center}
.send-btn{background:#000;color:#fff;border:none;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center}
#fileInput{display:none}
.speak-btn{font-size:12px;cursor:pointer;margin-top:5px;display:inline-block;color:#666}
</style>
</head>
<body>
<div class="header">
<div style="display:flex;align-items:center;gap:10px"><div class="logo">a</div><div><b>Andhariki AI</b><div style="font-size:12px;color:#666">Voice + Scanner ♻️</div></div></div>
<div style="font-size:11px;color:#666">Recycle Scanner ON</div>
</div>
<div class="chat" id="chat"><div class="msg ai">Hi! Nenu ready! 🎤 Voice tho matladu, 📷 Recycle item ni scan chey! ♻️</div></div>
<div class="input-area">
<div class="input-box">
<input id="inp" placeholder="Type or speak...">
<button class="icon-btn" onclick="startVoice()" id="voiceBtn">🎤</button>
<button class="icon-btn" onclick="document.getElementById('fileInput').click()">📷</button>
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<button class="send-btn" onclick="send()">↑</button>
</div>
</div>
<script>
const chat=document.getElementById('chat'); const inp=document.getElementById('inp');
let recognition;
function startVoice(){
 if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){alert('Voice ki Chrome vadandi');return;}
 const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
 recognition = new SR(); recognition.lang='te-IN'; recognition.interimResults=false;
 recognition.onstart=()=>{document.getElementById('voiceBtn').innerText='🔴'};
 recognition.onresult=(e)=>{inp.value=e.results[0][0].transcript; send();};
 recognition.onend=()=>{document.getElementById('voiceBtn').innerText='🎤'};
 recognition.start();
}
inp.addEventListener('keypress',e=>{if(e.key==='Enter')send()});
async function send(){
 let t=inp.value.trim(); if(!t)return;
 chat.innerHTML+=`<div class="msg user">${t}</div>`; inp.value=''; chat.scrollTop=chat.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  let id='s'+Date.now();
  chat.innerHTML+=`<div class="msg ai" id="${id}">${d.reply}<br><span class="speak-btn" onclick="speakText('${id}')">🔊 Vinu</span></div>`;
 }catch(e){ chat.innerHTML+=`<div class="msg ai">Network error</div>` }
 chat.scrollTop=chat.scrollHeight;
}
function speakText(id){
 let txt=document.getElementById(id).innerText.replace('🔊 Vinu','');
 let u=new SpeechSynthesisUtterance(txt); u.lang='te-IN'; u.rate=0.9; speechSynthesis.speak(u);
}
async function scanImage(event){
 let file=event.target.files[0]; if(!file)return;
 let reader=new FileReader();
 reader.onload=async function(){
  let base64=reader.result.split(',')[1];
  chat.innerHTML+=`<div class="msg user"><img src="${reader.result}" style="max-width:200px;border-radius:12px"><br>♻️ Scanning...</div>`;
  chat.scrollTop=chat.scrollHeight;
  let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:base64})});
  let d=await r.json();
  chat.innerHTML+=`<div class="msg ai">♻️ <b>Scanner Result:</b><br>${d.reply}<br><span class="speak-btn" onclick="speakText(this.parentElement.id)" id="sc${Date.now()}">🔊 Vinu</span></div>`;
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
                    json={"model": model,"messages": [{"role":"system","content":"You are Andhariki AI, helpful. Reply in user's language."},{"role":"user","content":user_msg}],"temperature":0.7,"max_tokens":1024},timeout=25)
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
    return jsonify({"reply":"Busy, 1 min taruvata try chey"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img_data = request.json.get("image","")
        if not GEMINI_API_KEY: return jsonify({"reply":"Scanner ki GEMINI_API_KEY add cheyali"})
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload={
            "contents":[{
                "parts":[
                    {"text":"You are a recycling scanner. Look at this image. Tell in Telugu + English: 1) What is this item? 2) Is it Recyclable ♻️ or Not? 3) Which bin? Blue/Green/Red? 4) How to recycle? Keep answer short, friendly, use emojis."},
                    {"inline_data":{"mime_type":"image/jpeg","data":img_data}}
                ]
            }]
        }
        res=requests.post(url,json=payload,timeout=30)
        data=res.json()
        text=data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply":text})
    except Exception as e:
        return jsonify({"reply":f"Scan failed: {str(e)[:100]} - Clear image pettu"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
