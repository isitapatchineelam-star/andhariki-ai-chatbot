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
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;height:100dvh;overflow:hidden}
.top{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;background:#000;border-bottom:1px solid #222;z-index:5}
.top-left{display:flex;align-items:center;gap:12px}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.getplus{background:#1e2a3a;color:#4a9eff;border-radius:20px;padding:8px 16px;font-size:13px;display:flex;align-items:center;gap:6px;font-weight:700}
.sidebar{position:fixed;top:0;left:-300px;width:280px;height:100%;background:#171717;z-index:20;transition:0.3s;padding:20px 0;display:flex;flex-direction:column}
.sidebar.open{left:0}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:15;display:none}
.overlay.show{display:block}
.side-item{display:flex;align-items:center;gap:14px;padding:14px 20px;color:#ececec;font-size:15px;cursor:pointer}
.side-item:hover{background:#2a2a2a}
.side-item i{width:24px;font-size:18px;color:#9e9e9e}
.side-top{padding:0 20px 20px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #2a2a2a;margin-bottom:10px}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:10px 14px;font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px;margin:10px 20px;cursor:pointer}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%;display:block}
.options{display:flex;flex-direction:column;gap:18px;margin:20% 0 20px 0;color:#8e8ea0;font-size:15px}
.opt{display:flex;align-items:center;gap:14px;cursor:pointer}
.msg{margin:12px 0;max-width:100%;line-height:1.7;font-size:15px;white-space:pre-wrap;word-break:break-word}
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
.q-label{font-weight:bold;color:#aaa;margin-top:14px;display:block;font-size:12px}
.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.gallery img{width:100%;border-radius:12px}
.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:8px 0}
</style>
</head>
<body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>
<div class="sidebar" id="sidebar">
<div class="side-top"><i class="fa-solid fa-sparkles" style="color:#4a9eff"></i><b>Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i> New chat</div>
<div class="side-item" onclick="showImages()"><i class="fa-regular fa-images"></i> Images</div>
<div class="side-item" onclick="showLibrary()"><i class="fa-solid fa-book-open"></i> Library</div>
<div class="side-item" onclick="showProjects()"><i class="fa-regular fa-folder"></i> Projects</div>
<div class="side-item" onclick="showScheduled()"><i class="fa-regular fa-clock"></i> Scheduled</div>
<div class="side-item" onclick="showPlugins()"><i class="fa-solid fa-plug"></i> Plugins</div>
<div style="margin-top:auto;padding:20px;color:#666;font-size:12px">♻️ Andhariki AI</div>
</div>
<div class="top">
<div class="top-left"><div class="menu" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i></div><div class="getplus"><i class="fa-solid fa-sparkles"></i> Andhariki AI</div></div>
<div class="menu" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i></div>
</div>
<div class="chat" id="chat">
<div class="options" id="opts">
<div class="opt" onclick="quick('Create an image of recycling bin')"><i class="fa-regular fa-image"></i> Create an image</div>
<div class="opt" onclick="quick('Write a post about recycling')"><i class="fa-solid fa-pen"></i> Write or edit</div>
<div class="opt" onclick="quick('Search about waste management')"><i class="fa-solid fa-globe"></i> Search the web</div>
</div>
<div id="mainContent"></div>
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
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function newChat(){document.getElementById('mainContent').innerHTML='';document.getElementById('opts').style.display='flex';toggleMenu();}
function showImages(){toggleMenu();document.getElementById('opts').style.display='none';let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');let html='<div class="q-label">IMAGES GALLERY</div><div class="gallery">';if(imgs.length==0)html+='<p style="color:#888">Inka images levu.</p>';imgs.forEach(s=>{html+=`<img src="${s}">`});html+='</div>';document.getElementById('mainContent').innerHTML=html;}
function showLibrary(){toggleMenu();document.getElementById('opts').style.display='none';let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');let html='<div class="q-label">LIBRARY</div>';if(chats.length==0)html+='<p style="color:#888">Chat history ledu</p>';chats.slice(-20).reverse().forEach(c=>{html+=`<div class="card"><b>You:</b> ${c.q}<br><span style="color:#aaa">${c.a.substring(0,80)}...</span></div>`});document.getElementById('mainContent').innerHTML=html;}
function showProjects(){toggleMenu();document.getElementById('opts').style.display='none';document.getElementById('mainContent').innerHTML=`<div class="q-label">PROJECTS</div><div class="card">♻️ <b>Recycle Bin Scanner</b></div>`;}
function showScheduled(){toggleMenu();document.getElementById('opts').style.display='none';document.getElementById('mainContent').innerHTML=`<div class="q-label">SCHEDULED</div><div class="card">⏰ Ready</div>`;}
function showPlugins(){toggleMenu();document.getElementById('opts').style.display='none';document.getElementById('mainContent').innerHTML=`<div class="q-label">PLUGINS</div><div class="card">📷 Scanner ON<br>🎤 Voice ON</div>`;}
const chat=document.getElementById('chat'); const inp=document.getElementById('inp');
function quick(t){inp.value=t; send();}
function startVoice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;let rec=new SR();rec.lang='te-IN';rec.onresult=(e)=>{inp.value=e.results[0][0].transcript;send();};rec.start();}
async function send(){
 let t=inp.value.trim(); if(!t) return;
 document.getElementById('opts').style.display='none';
 document.getElementById('mainContent').innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div>`;
 inp.value=''; chat.scrollTop=chat.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  document.getElementById('mainContent').innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;
  let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]'); chats.push({q:t,a:d.reply}); localStorage.setItem('ai_chats',JSON.stringify(chats));
 }catch(e){ document.getElementById('mainContent').innerHTML+=`<div class="msg ai">Network error</div>` }
 chat.scrollTop=chat.scrollHeight;
}
async function scanImage(e){
 let file=e.target.files[0]; if(!file) return;
 let reader=new FileReader();
 reader.onload=async()=>{
  let b64=reader.result.split(',')[1];
  document.getElementById('opts').style.display='none';
  document.getElementById('mainContent').innerHTML+=`<div class="q-label">You</div><div class="msg user"><img src="${reader.result}" style="max-width:200px;border-radius:12px"><br>♻️ Scanning...</div>`;
  let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]'); imgs.push(reader.result); localStorage.setItem('ai_images',JSON.stringify(imgs.slice(-20)));
  try{
   let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});
   let d=await r.json();
   document.getElementById('mainContent').innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">♻️ ${d.reply}</div>`;
  }catch(err){ document.getElementById('mainContent').innerHTML+=`<div class="msg ai">❌ Scan error</div>` }
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
        for m in ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]:
            try:
                r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},json={"model":m,"messages":[{"role":"system","content":"You are Andhariki AI, friendly Telugu+English mix."},{"role":"user","content":msg}],"max_tokens":1024},timeout=20)
                j=r.json()
                if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except: continue
    if GEMINI_API_KEY:
        for mn in ["gemini-2.5-flash","gemini-1.5-flash"]:
            try:
                url=f"https://generativelanguage.googleapis.com/v1beta/models/{mn}:generateContent?key={GEMINI_API_KEY}"
                r=requests.post(url,json={"contents":[{"parts":[{"text":msg}]}]},timeout=20)
                j=r.json()
                if "candidates" in j: return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
            except: continue
    return jsonify({"reply":"Busy, malli adugu"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img=request.json.get("image","")
        prompt_text="You are Andhariki AI recycling expert. Analyze image in Telugu+English mix with emojis. Format: 1) Idi enti? 2) Recyclable ah? 3) E bin? 4) Ela recycle cheyali? If animal/person/food, say 'Idi living thing raa, recycle kaadu' with fun fact. Short 4-5 lines."

        # 1. GROQ VISION - FAST, NO BUSY ERROR
        if GROQ_API_KEY:
            for m in ["meta-llama/llama-4-scout-17b-16e-instruct","meta-llama/llama-4-maverick-17b-128e-instruct","llama-3.2-11b-vision-preview"]:
                try:
                    r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt_text},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":600},timeout=30)
                    j=r.json()
                    print(f"Groq {m}: {str(j)[:400]}")
                    if "choices" in j and len(j["choices"])>0:
                        return jsonify({"reply":j["choices"][0]["message"]["content"]})
                except Exception as e:
                    print(f"Groq {m} fail {e}")
                    continue

        # 2. GEMINI BACKUP
        if GEMINI_API_KEY:
            for mn in ["gemini-2.5-flash","gemini-1.5-flash","gemini-flash-latest"]:
                try:
                    url=f"https://generativelanguage.googleapis.com/v1beta/models/{mn}:generateContent?key={GEMINI_API_KEY}"
                    r=requests.post(url,json={"contents":[{"parts":[{"text":prompt_text},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]},timeout=30)
                    j=r.json()
                    if "candidates" in j and j["candidates"]:
                        return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
                except: continue

        return jsonify({"reply":"♻️ Server konchem busy raa babooie, 30 sec tarvata malli try chey!"})
    except Exception as e:
        return jsonify({"reply":f"Error {e}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
