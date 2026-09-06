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
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;height:100dvh}
.top{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;background:#000;border-bottom:1px solid #222}
.top-left{display:flex;align-items:center;gap:12px}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.getplus{background:#1e2a3a;color:#4a9eff;border-radius:20px;padding:8px 16px;font-size:13px;display:flex;align-items:center;gap:6px;font-weight:700}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%;display:block}
.options{display:flex;flex-direction:column;gap:18px;margin:30% 0 20px 0;color:#8e8ea0;font-size:15px}
.opt{display:flex;align-items:center;gap:14px;cursor:pointer}
.msg{margin:16px 0;padding:0;background:transparent;max-width:100%;line-height:1.7;font-size:15px;white-space:pre-wrap;word-break:break-word}
.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}
.msg.ai{color:#ececec;padding:8px 4px}
.input-area{padding:10px 12px 18px;background:#000;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:10px;min-height:50px;border:1px solid #3a3a3a}
.input-box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.input-box input::placeholder{color:#8e8ea0}
.plus{width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:18px;color:#8e8ea0;cursor:pointer}
.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer;flex-shrink:0}
.mic{font-size:18px;color:#8e8ea0;cursor:pointer;padding:6px}
#fileInput{display:none}
.q-label{font-weight:bold;color:#fff;margin-top:12px;display:block;font-size:15px}
</style>
</head>
<body>
<div class="top">
<div class="top-left"><div class="menu"><i class="fa-solid fa-bars"></i></div><div class="getplus"><i class="fa-solid fa-sparkles"></i> Andhariki AI</div></div>
<div class="menu"><i class="fa-solid fa-ellipsis"></i></div>
</div>

<div class="chat" id="chat">
<div class="options" id="opts">
<div class="opt" onclick="quick('Create an image of a recycling bin')"><i class="fa-regular fa-image"></i> Create an image or sticker</div>
<div class="opt" onclick="quick('Write or edit a post about recycling')"><i class="fa-solid fa-pen"></i> Write or edit</div>
<div class="opt" onclick="quick('Search the web about waste management')"><i class="fa-solid fa-globe"></i> Search the web</div>
</div>
</div>

<div class="input-area">
<div class="input-box">
<div class="plus" onclick="document.getElementById('fileInput').click()"><i class="fa-solid fa-plus"></i></div>
<input id="inp" placeholder="Ask Andhariki AI ♻️" onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<i class="fa-solid fa-microphone mic" onclick="startVoice()"></i>
<div class="voice-circle" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div>
</div>

<script>
const chat=document.getElementById('chat'); const inp=document.getElementById('inp');
function quick(t){ inp.value=t; send(); }
let recognition;
function startVoice(){
 if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){ alert('Chrome lo open chey'); return; }
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 recognition=new SR(); recognition.lang='te-IN';
 recognition.onresult=(e)=>{ inp.value=e.results[0][0].transcript; send(); };
 recognition.start();
}
async function send(){
 let t=inp.value.trim(); if(!t) return;
 document.getElementById('opts').style.display='none';
 // NEE QUESTION IPPUDU CLEAR GA KANIPISTADI
 chat.innerHTML+=`<div class="q-label">You:</div><div class="msg user">${t}</div>`;
 inp.value='';
 setTimeout(()=>{ chat.scrollTop=chat.scrollHeight; },50);
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  chat.innerHTML+=`<div class="q-label">Andhariki AI:</div><div class="msg ai">${d.reply}</div><hr style="border:none;border-top:1px solid #222;margin:20px 0">`;
 }catch(e){ chat.innerHTML+=`<div class="msg ai">Network error</div>` }
 chat.scrollTop=chat.scrollHeight;
}
async function scanImage(e){
 let file=e.target.files[0]; if(!file) return;
 let reader=new FileReader();
 reader.onload=async()=>{
  let b64=reader.result.split(',')[1];
  document.getElementById('opts').style.display='none';
  chat.innerHTML+=`<div class="q-label">You:</div><div class="msg user"><img src="${reader.result}" style="max-width:200px;border-radius:12px"><br>♻️ Scan chestunna...</div>`;
  let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});
  let d=await r.json();
  chat.innerHTML+=`<div class="q-label">Andhariki AI:</div><div class="msg ai">♻️ ${d.reply}</div>`;
  chat.scrollTop=chat.scrollHeight;
 };
 reader.readAsDataURL(file);
}
</script>
</body>
</html>
"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg=request.json.get("message","")
    if GROQ_API_KEY:
        for m in ["openai/gpt-oss-20b","openai/gpt-oss-120b"]:
            try:
                r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},json={"model":m,"messages":[{"role":"system","content":"You are Andhariki AI, friendly, reply in user's language."},{"role":"user","content":msg}],"max_tokens":1024},timeout=25)
                j=r.json()
                if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except: continue
    if GEMINI_API_KEY:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r=requests.post(url,json={"contents":[{"parts":[{"text":msg}]}]},timeout=25)
            j=r.json()
            if "candidates" in j: return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass
    return jsonify({"reply":"Busy, malli adugu"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img=request.json.get("image","")
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload={"contents":[{"parts":[{"text":"You are Andhariki AI recycling scanner. Analyze image: what item, recyclable?, which bin?, how to recycle? Short Telugu+English."},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]}
        r=requests.post(url,json=payload,timeout=30)
        j=r.json()
        return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
    except: return jsonify({"reply":"Clear photo petti malli try chey"})

if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
