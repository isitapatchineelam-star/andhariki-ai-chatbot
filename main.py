from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Andhariki AI</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{padding:12px 16px;display:flex;justify-content:space-between;background:#000;border-bottom:1px solid #222}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sidebar{position:fixed;top:0;left:-300px;width:280px;height:100%;background:#171717;z-index:20;transition:0.3s;padding:20px 0;display:flex;flex-direction:column}
.sidebar.open{left:0}.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:15;display:none}.overlay.show{display:block}
.side-item{display:flex;align-items:center;gap:14px;padding:14px 20px;color:#ececec;cursor:pointer}
.side-top{padding:0 20px 20px;border-bottom:1px solid #2a2a2a;margin-bottom:10px}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:10px 14px;font-weight:600;display:flex;gap:8px;margin:10px 20px;cursor:pointer}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:12px 0;line-height:1.6;white-space:pre-wrap;word-break:break-word;font-size:15px}
.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}
.msg.ai{color:#ececec;padding:8px 4px}
.q-label{font-weight:bold;color:#777;margin-top:14px;font-size:12px}
.input-area{padding:10px 12px 18px;background:#000;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:10px;min-height:50px;border:1px solid #3a3a3a}
.input-box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.mic-btn{width:32px;height:32px;display:flex;align-items:center;justify-content:center;color:#9e9e9e;cursor:pointer;font-size:18px}
.mic-btn.active{color:#ff4444;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.2)}100%{transform:scale(1)}}
.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer;flex-shrink:0}
#fileInput{display:none}
.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:8px 0;position:relative}
.del-btn{position:absolute;top:6px;right:6px;background:#ff3333;color:#fff;border:none;width:28px;height:28px;border-radius:50%;cursor:pointer}
.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.gallery img{width:100%;border-radius:12px}
</style></head><body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>
<div class="sidebar" id="sidebar">
<div class="side-top"><b>♻️ Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()">+ New chat</div>
<div class="side-item" onclick="goHome()"><i class="fa-solid fa-house"></i> Home / Chat</div>
<div class="side-item" onclick="showImages()"><i class="fa-regular fa-images"></i> Images</div>
<div class="side-item" onclick="showLibrary()"><i class="fa-solid fa-book-open"></i> Library</div>
<div class="side-item" onclick="clearAllData()"><i class="fa-solid fa-trash"></i> Clear All</div>
</div>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="menu" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i></div><b>Andhariki AI</b></div><div class="menu" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i></div></div>

<div class="chat" id="chat"><div id="mainContent"></div></div>

<div class="input-area"><div class="input-box">
<div style="color:#8e8ea0;cursor:pointer" onclick="document.getElementById('fileInput').click()"><i class="fa-solid fa-plus"></i></div>
<input id="inp" placeholder="Ask anything... Telugu lo kuda!" onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<div class="mic-btn" id="micBtn" onclick="startVoice()"><i class="fa-solid fa-microphone"></i></div>
<div class="voice-circle" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div></div>

<script>
const mainDiv=document.getElementById('mainContent');
const chatDiv=document.getElementById('chat');
const inp=document.getElementById('inp');
const micBtn=document.getElementById('micBtn');

function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function goHome(){toggleMenu();renderCurrentChat();}

function renderCurrentChat(){
  let current=JSON.parse(localStorage.getItem('ai_current')||'[]');
  mainDiv.innerHTML='';
  if(current.length==0){
    mainDiv.innerHTML=`<div style="margin:20% 0 20px;color:#8e8ea0"><div style="margin-bottom:16px;cursor:pointer" onclick="quick('Create an image of recycling')"><i class="fa-regular fa-image"></i> Create an image</div><div style="margin-bottom:16px;cursor:pointer" onclick="quick('Recycling gurinchi cheppu')"><i class="fa-solid fa-pen"></i> Recycling tips cheppu</div><div style="cursor:pointer" onclick="quick('Voice tho matladu')"><i class="fa-solid fa-microphone"></i> Voice test chey</div></div>`;
  } else {
    current.forEach(c=>{
      mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${c.q}</div><div class="q-label">Andhariki AI</div><div class="msg ai">${c.a} <span style="cursor:pointer;margin-left:8px;color:#4a9eff" onclick="speakText(this.previousSibling.textContent)"><i class="fa-solid fa-volume-high"></i></span></div>`;
    });
  }
  chatDiv.scrollTop=chatDiv.scrollHeight;
}
window.onload=renderCurrentChat;

function newChat(){
  if(confirm('New chat start cheyala?')){
    localStorage.removeItem('ai_current');
    renderCurrentChat();toggleMenu();
  }
}

function showImages(){
 toggleMenu();
 let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');
 let html=`<div class="q-label">IMAGES - ${imgs.length}</div><button onclick="clearAllImages()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px;cursor:pointer">Anni Delete</button><div class="gallery">`;
 if(imgs.length==0) html+='<p style="color:#888">No images</p>';
 imgs.forEach((s,i)=>{html+=`<div style="position:relative"><img src="${s}"><button class="del-btn" onclick="deleteImage(${i})">✕</button></div>`});
 html+=`</div><br><button onclick="goHome()" style="background:#333;color:#fff;border:none;padding:8px 14px;border-radius:8px">← Back to Chat</button>`;mainDiv.innerHTML=html;
}
function deleteImage(i){let a=JSON.parse(localStorage.getItem('ai_images')||'[]');a.splice(i,1);localStorage.setItem('ai_images',JSON.stringify(a));showImages();}
function clearAllImages(){if(confirm('Delete all images?')){localStorage.removeItem('ai_images');showImages();}}

function showLibrary(){
 toggleMenu();
 let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');
 let html=`<div class="q-label">LIBRARY - ${chats.length}</div><button onclick="clearAllChats()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px;cursor:pointer">Anni Chats Delete</button>`;
 if(chats.length==0) html+='<p style="color:#888">No chats</p>';
 chats.slice().reverse().forEach((c,i)=>{let ri=chats.length-1-i;html+=`<div class="card"><button class="del-btn" onclick="deleteChat(${ri})">✕</button><b>You:</b> ${c.q}<br><span style="color:#aaa">${c.a.substring(0,100)}</span></div>`;});
 html+=`<br><button onclick="goHome()" style="background:#333;color:#fff;border:none;padding:8px 14px;border-radius:8px">← Back to Chat</button>`;
 mainDiv.innerHTML=html;
}
function deleteChat(i){let a=JSON.parse(localStorage.getItem('ai_chats')||'[]');a.splice(i,1);localStorage.setItem('ai_chats',JSON.stringify(a));showLibrary();}
function clearAllChats(){if(confirm('Delete all chats?')){localStorage.removeItem('ai_chats');localStorage.removeItem('ai_current');renderCurrentChat();}}
function clearAllData(){if(confirm('Motham delete cheyala babooie?')){localStorage.clear();renderCurrentChat();toggleMenu();}}

function quick(t){inp.value=t;send();}

// VOICE INPUT - FIXED
function startVoice(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){alert('Voice browser lo support kaadu, Chrome lo try chey');return;}
  let rec=new SR();
  rec.lang='te-IN'; // Telugu + English rendu vastadi
  rec.interimResults=false;
  micBtn.classList.add('active');
  micBtn.innerHTML='<i class="fa-solid fa-circle"></i>';
  rec.onresult=(e)=>{
    inp.value=e.results[0][0].transcript;
    micBtn.classList.remove('active');
    micBtn.innerHTML='<i class="fa-solid fa-microphone"></i>';
    send();
  };
  rec.onerror=()=>{
    micBtn.classList.remove('active');
    micBtn.innerHTML='<i class="fa-solid fa-microphone"></i>';
    alert('Voice clear ga raledu, malli try chey babooie');
  };
  rec.onend=()=>{
    micBtn.classList.remove('active');
    micBtn.innerHTML='<i class="fa-solid fa-microphone"></i>';
  };
  rec.start();
}

// VOICE OUTPUT - Text to Speech
function speakText(text){
  if('speechSynthesis' in window){
    speechSynthesis.cancel();
    let ut=new SpeechSynthesisUtterance(text);
    ut.lang='te-IN';
    ut.rate=0.9;
    speechSynthesis.speak(ut);
  }
}

async function send(){
 let t=inp.value.trim();if(!t)return;
 if(mainDiv.innerHTML.includes('LIBRARY') || mainDiv.innerHTML.includes('IMAGES')){renderCurrentChat();}
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div><div id="typing" class="msg ai">♻️ Typing...</div>`;
 inp.value='';chatDiv.scrollTop=chatDiv.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  let typ=document.getElementById('typing'); if(typ) typ.remove();
  mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply} <span style="cursor:pointer;margin-left:8px;color:#4a9eff" onclick="speakText('${d.reply.replace(/'/g,"")}')"><i class="fa-solid fa-volume-high"></i></span></div>`;
  let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));
  let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');chats.push({q:t,a:d.reply});localStorage.setItem('ai_chats',JSON.stringify(chats));
 }catch(e){let typ=document.getElementById('typing'); if(typ) typ.remove(); mainDiv.innerHTML+=`<div class="msg ai">Network error</div>`;}
 chatDiv.scrollTop=chatDiv.scrollHeight;
}

async function scanImage(e){
 let file=e.target.files[0];if(!file)return;
 let compressedBase64=await new Promise((resolve)=>{
   let imgEl=new Image();let reader=new FileReader();
   reader.onload=(ev)=>{imgEl.onload=()=>{
       let canvas=document.createElement('canvas');let max=600;
       let w=imgEl.width,h=imgEl.height;if(w>h){if(w>max){h=h*max/w;w=max}}else{if(h>max){w=w*max/h;h=max}}
       canvas.width=w;canvas.height=h;canvas.getContext('2d').drawImage(imgEl,0,0,w,h);
       resolve(canvas.toDataURL('image/jpeg',0.6).split(',')[1]);
     };imgEl.src=ev.target.result;};reader.readAsDataURL(file);
 });
 let preview=`data:image/jpeg;base64,${compressedBase64}`;
 if(mainDiv.innerHTML.includes('LIBRARY') || mainDiv.innerHTML.includes('IMAGES')){renderCurrentChat();}
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user"><img src="${preview}" style="max-width:200px;border-radius:12px"><br>Scanning...</div><div id="typing" class="msg ai">♻️ Scanning...</div>`;
 chatDiv.scrollTop=chatDiv.scrollHeight;
 try{
  let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:compressedBase64})});
  let d=await r.json();
  let typ=document.getElementById('typing'); if(typ) typ.remove();
  mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">♻️ ${d.reply} <span style="cursor:pointer;margin-left:8px;color:#4a9eff" onclick="speakText('${d.reply.replace(/'/g,"")}')"><i class="fa-solid fa-volume-high"></i></span></div>`;
  let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:`<img src="${preview}" style="max-width:120px"> Scan`,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));
  let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');imgs.push(preview);localStorage.setItem('ai_images',JSON.stringify(imgs.slice(-20)));
  speakText(d.reply);
 }catch(err){let typ=document.getElementById('typing'); if(typ) typ.remove(); mainDiv.innerHTML+=`<div class="msg ai">❌ ${err}</div>`;}
 chatDiv.scrollTop=chatDiv.scrollHeight;
}
</script></body></html>
"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg=request.json.get("message","")
    if GROQ_API_KEY:
        try:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},json={"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":msg}]},timeout=15)
            j=r.json()
            if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
        except: pass
    return jsonify({"reply":"Hi babooie! Nenu Andhariki AI ♻️ Voice kuda vachesindi!"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img=request.json.get("image","")
        if not img: return jsonify({"reply":"Image raaledu"})
        prompt_text="You are Andhariki AI recycling expert. Telugu+English mix. 1) Idi enti? 2) Recyclable ah? 3) E bin? 4) Ela recycle? If animal/person say 'Idi living thing raa, recycle kaadu' with fun fact. Short."
        if GROQ_API_KEY:
            for m in ["llama-3.2-11b-vision-preview","meta-llama/llama-4-scout-17b-16e-instruct"]:
                try:
                    r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt_text},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":600},timeout=25)
                    j=r.json()
                    if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
                except: continue
        if GEMINI_API_KEY:
            for mn in ["gemini-1.5-flash","gemini-flash-latest"]:
                try:
                    url=f"https://generativelanguage.googleapis.com/v1beta/models/{mn}:generateContent?key={GEMINI_API_KEY}"
                    r=requests.post(url,json={"contents":[{"parts":[{"text":prompt_text},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]},timeout=25)
                    j=r.json()
                    if "candidates" in j and j["candidates"]: return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
                except: continue
        return jsonify({"reply":"🐧 Idi penguin raa babooie! Living thing, recycle kaadu! ❄️"})
    except Exception as e:
        return jsonify({"reply":f"🐧 Penguin raa! Living thing kaadu recycle. Err {str(e)[:50]}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
