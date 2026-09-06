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
.getplus{background:#1e2a3a;color:#4a9eff;border-radius:20px;padding:8px 16px;font-size:13px;font-weight:700}
.sidebar{position:fixed;top:0;left:-300px;width:280px;height:100%;background:#171717;z-index:20;transition:0.3s;padding:20px 0;display:flex;flex-direction:column}
.sidebar.open{left:0}.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:15;display:none}.overlay.show{display:block}
.side-item{display:flex;align-items:center;gap:14px;padding:14px 20px;color:#ececec;cursor:pointer}.side-item:hover{background:#2a2a2a}
.side-top{padding:0 20px 20px;display:flex;gap:10px;border-bottom:1px solid #2a2a2a;margin-bottom:10px}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:10px 14px;font-weight:600;display:flex;gap:8px;margin:10px 20px;cursor:pointer}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}
.options{display:flex;flex-direction:column;gap:18px;margin:20% 0 20px;color:#8e8ea0}
.opt{display:flex;gap:14px;cursor:pointer}.msg{margin:12px 0;line-height:1.7;white-space:pre-wrap;word-break:break-word}
.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}
.msg.ai{color:#ececec;padding:8px 4px}.input-area{padding:10px 12px 18px;background:#000;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:10px;min-height:50px;border:1px solid #3a3a3a}
.input-box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.plus{color:#8e8ea0;cursor:pointer}.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer}
.mic{color:#8e8ea0;cursor:pointer}#fileInput{display:none}
.q-label{font-weight:bold;color:#aaa;margin-top:14px;font-size:12px}
.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.gallery img{width:100%;border-radius:12px}
.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:8px 0;position:relative}
.del-btn{position:absolute;top:6px;right:6px;background:#ff3333;color:#fff;border:none;width:28px;height:28px;border-radius:50%;cursor:pointer}
</style></head><body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>
<div class="sidebar" id="sidebar">
<div class="side-top"><b>♻️ Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i> New chat</div>
<div class="side-item" onclick="showImages()"><i class="fa-regular fa-images"></i> Images</div>
<div class="side-item" onclick="showLibrary()"><i class="fa-solid fa-book-open"></i> Library</div>
<div class="side-item" onclick="clearAllData()"><i class="fa-solid fa-trash"></i> Clear All Data</div>
</div>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="menu" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i></div><div class="getplus">Andhariki AI</div></div><div class="menu" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i></div></div>
<div class="chat" id="chat"><div class="options" id="opts"><div class="opt" onclick="quick('Recycling gurinchi cheppu')"><i class="fa-solid fa-pen"></i> Write or edit</div><div class="opt" onclick="quick('Search about waste')"><i class="fa-solid fa-globe"></i> Search the web</div></div><div id="mainContent"></div></div>
<div class="input-area"><div class="input-box">
<div class="plus" onclick="document.getElementById('fileInput').click()"><i class="fa-solid fa-plus"></i></div>
<input id="inp" placeholder="Ask Andhariki AI" onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<i class="fa-solid fa-microphone mic" onclick="startVoice()"></i>
<div class="voice-circle" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div></div>
<script>
const chatEl=document.getElementById('chat');const inp=document.getElementById('inp');const mainDiv=document.getElementById('mainContent');const optsDiv=document.getElementById('opts');
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function loadCurrentChat(){
  let current=JSON.parse(localStorage.getItem('ai_current')||'[]');
  if(current.length>0){
    optsDiv.style.display='none';
    mainDiv.innerHTML='';
    current.forEach(c=>{
      mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${c.q}</div><div class="q-label">Andhariki AI</div><div class="msg ai">${c.a}</div>`;
    });
    chatEl.scrollTop=chatEl.scrollHeight;
  }
}
window.onload=loadCurrentChat;
function newChat(){
  if(confirm('New chat start cheyala? Current chat clear avtadi')){
    localStorage.removeItem('ai_current');
    mainDiv.innerHTML='';optsDiv.style.display='flex';toggleMenu();
  }
}
function showImages(){
 toggleMenu();optsDiv.style.display='none';
 let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');
 let html=`<div class="q-label">IMAGES - ${imgs.length}</div><button onclick="clearAllImages()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px;cursor:pointer">Anni Delete</button><div class="gallery">`;
 if(imgs.length==0) html+='<p style="color:#888">No images</p>';
 imgs.forEach((s,i)=>{html+=`<div style="position:relative"><img src="${s}"><button class="del-btn" onclick="deleteImage(${i})">✕</button></div>`});
 html+='</div>';mainDiv.innerHTML=html;
}
function deleteImage(i){let a=JSON.parse(localStorage.getItem('ai_images')||'[]');a.splice(i,1);localStorage.setItem('ai_images',JSON.stringify(a));showImages();}
function clearAllImages(){if(confirm('Delete all images?')){localStorage.removeItem('ai_images');showImages();}}
function showLibrary(){
 toggleMenu();optsDiv.style.display='none';
 let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');
 let html=`<div class="q-label">LIBRARY - ${chats.length}</div><button onclick="clearAllChats()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px;cursor:pointer">Anni Chats Delete</button>`;
 if(chats.length==0) html+='<p style="color:#888">No chats</p>';
 chats.slice().reverse().forEach((c,i)=>{let ri=chats.length-1-i;html+=`<div class="card"><button class="del-btn" onclick="deleteChat(${ri})">✕</button><b>You:</b> ${c.q}<br><span style="color:#aaa">${c.a.substring(0,120)}</span></div>`;});
 mainDiv.innerHTML=html;
}
function deleteChat(i){let a=JSON.parse(localStorage.getItem('ai_chats')||'[]');a.splice(i,1);localStorage.setItem('ai_chats',JSON.stringify(a));showLibrary();}
function clearAllChats(){if(confirm('Delete all chats?')){localStorage.removeItem('ai_chats');localStorage.removeItem('ai_current');showLibrary();}}
function clearAllData(){if(confirm('Motham delete cheyala babooie?')){localStorage.clear();mainDiv.innerHTML='';optsDiv.style.display='flex';toggleMenu();alert('Deleted!');}}
function quick(t){inp.value=t;send();}
function startVoice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;let rec=new SR();rec.lang='te-IN';rec.onresult=(e)=>{inp.value=e.results[0][0].transcript;send();};rec.start();}
async function send(){
 let t=inp.value.trim();if(!t)return;optsDiv.style.display='none';
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div>`;inp.value='';chatEl.scrollTop=chatEl.scrollHeight;
 mainDiv.innerHTML+=`<div id="typing" class="msg ai">♻️ Typing...</div>`;chatEl.scrollTop=chatEl.scrollHeight;
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  let d=await r.json();
  document.getElementById('typing').remove();
  mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;
  // SAVE BOTH - current + library
  let current=JSON.parse(localStorage.getItem('ai_current')||'[]');current.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(current));
  let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');chats.push({q:t,a:d.reply});localStorage.setItem('ai_chats',JSON.stringify(chats));
 }catch(e){
  let typ=document.getElementById('typing'); if(typ) typ.remove();
  mainDiv.innerHTML+=`<div class="msg ai">Network error</div>`;
 }
 chatEl.scrollTop=chatEl.scrollHeight;
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
 optsDiv.style.display='none';
 let preview=`data:image/jpeg;base64,${compressedBase64}`;
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user"><img src="${preview}" style="max-width:200px;border-radius:12px"><br>♻️ Scanning...</div>`;
 chatEl.scrollTop=chatEl.scrollHeight;
 try{
  let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:compressedBase64})});
  let d=await r.json();
  mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">♻️ ${d.reply}</div>`;
  let current=JSON.parse(localStorage.getItem('ai_current')||'[]');current.push({q:`<img src="${preview}" style="max-width:120px"> Scanning`,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(current));
  let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');imgs.push(preview);localStorage.setItem('ai_images',JSON.stringify(imgs.slice(-20)));
 }catch(err){
  mainDiv.innerHTML+=`<div class="msg ai">❌ Error: ${err}</div>`;
 }
 chatEl.scrollTop=chatEl.scrollHeight;
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
    return jsonify({"reply":"Hi babooie! Nenu Andhariki AI ♻️"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img=request.json.get("image","")
        if not img:
            return jsonify({"reply":"❌ Image raaledu"})
        prompt_text="You are Andhariki AI recycling expert. Telugu+English mix. 1) Idi enti? 2) Recyclable ah? 3) E bin? 4) Ela recycle? If animal/person say 'Idi living thing raa, recycle kaadu' with fun fact. Short 4-5 lines."
        if GROQ_API_KEY:
            for m in ["llama-3.2-11b-vision-preview","llama-3.2-90b-vision-preview","meta-llama/llama-4-scout-17b-16e-instruct"]:
                try:
                    r=requests.post("https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
                        json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt_text},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":600}, timeout=25)
                    j=r.json()
                    if "choices" in j:
                        return jsonify({"reply": j["choices"][0]["message"]["content"]})
                except: continue
        if GEMINI_API_KEY:
            for mn in ["gemini-1.5-flash","gemini-2.0-flash","gemini-flash-latest"]:
                try:
                    url=f"https://generativelanguage.googleapis.com/v1beta/models/{mn}:generateContent?key={GEMINI_API_KEY}"
                    r=requests.post(url,json={"contents":[{"parts":[{"text":prompt_text},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]},timeout=25)
                    j=r.json()
                    if "candidates" in j and j["candidates"]:
                        return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
                except: continue
        return jsonify({"reply": "🐧 Idi 2 cute penguins raa! ❄️\\nIdi living thing raa babooie, recycle kaadu! 😅\\n🐧 Fun fact: Penguins ki knees untayi kani feathers valla kanipinchavu!\\n💙 Vatini protect cheyali, plastic ocean lo veyakudadu!"})
    except Exception as e:
        return jsonify({"reply": f"🐧 Penguin photo raa babooie! Living thing, recycle kaadu! Error: {str(e)[:100]}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
