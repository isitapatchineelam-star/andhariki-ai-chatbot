from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Andhariki AI</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{padding:12px 16px;display:flex;justify-content:space-between;background:#000;border-bottom:1px solid #222}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sidebar{position:fixed;top:0;left:-300px;width:280px;height:100%;background:#171717;z-index:20;transition:0.3s;padding:20px 0;display:flex;flex-direction:column}
.sidebar.open{left:0}.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6);z-index:15;display:none}.overlay.show{display:block}
.side-item{display:flex;align-items:center;gap:14px;padding:14px 20px;color:#ececec;cursor:pointer}.side-item:hover{background:#2a2a2a}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:10px 14px;font-weight:600;display:flex;gap:8px;margin:10px 20px;cursor:pointer}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:12px 0;line-height:1.7;white-space:pre-wrap;word-break:break-word}
.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}
.msg.ai{color:#ececec;padding:8px 4px}.q-label{font-weight:bold;color:#777;margin-top:14px;font-size:12px}
.input-area{padding:10px 12px 18px;background:#000;position:sticky;bottom:0}
.input-box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:10px;min-height:50px;border:1px solid #3a3a3a}
.input-box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.mic-btn{width:32px;height:32px;display:flex;align-items:center;justify-content:center;color:#9e9e9e;cursor:pointer;font-size:18px}.mic-btn.active{color:#ff4444;animation:pulse 1s infinite}@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.2)}100%{transform:scale(1)}}
.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer;flex-shrink:0}
#fileInput{display:none}.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:8px 0;position:relative}.del-btn{position:absolute;top:6px;right:6px;background:#ff3333;color:#fff;border:none;width:28px;height:28px;border-radius:50%;cursor:pointer}.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.gallery img{width:100%;border-radius:12px}
</style></head><body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>
<div class="sidebar" id="sidebar">
<div style="padding:0 20px 20px;border-bottom:1px solid #2a2a2a;margin-bottom:10px"><b>♻️ Andhariki AI</b></div>
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
<input id="inp" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<div class="mic-btn" id="micBtn" onclick="startVoice()"><i class="fa-solid fa-microphone"></i></div>
<div class="voice-circle" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div></div>
<script>
const mainDiv=document.getElementById('mainContent'),chatDiv=document.getElementById('chat'),inp=document.getElementById('inp'),micBtn=document.getElementById('micBtn');
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function goHome(){toggleMenu();renderCurrentChat();}
function renderCurrentChat(){
  let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');
  mainDiv.innerHTML='';
  if(cur.length==0){
    mainDiv.innerHTML=`<div style="margin:20% 0;color:#8e8ea0"><div style="margin-bottom:14px;cursor:pointer" onclick="quick('Recycling gurinchi cheppu')"><i class="fa-solid fa-pen"></i> Recycling tips cheppu</div><div style="margin-bottom:14px;cursor:pointer" onclick="quick('Plastic ela recycle cheyali?')"><i class="fa-solid fa-recycle"></i> Plastic recycling</div><div style="cursor:pointer" onclick="document.getElementById('fileInput').click()"><i class="fa-regular fa-image"></i> Photo scan chey</div></div>`;
  } else {
    cur.forEach(c=>{mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${c.q}</div><div class="q-label">Andhariki AI</div><div class="msg ai">${c.a} <span style="cursor:pointer;color:#4a9eff" onclick="speakText(this.parentElement.innerText)"><i class="fa-solid fa-volume-high"></i></span></div>`;});
  }
  chatDiv.scrollTop=chatDiv.scrollHeight;
}
window.onload=renderCurrentChat;
function newChat(){if(confirm('New chat start cheyala?')){localStorage.removeItem('ai_current');renderCurrentChat();toggleMenu();}}
function showImages(){toggleMenu();let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');let html=`<div class="q-label">IMAGES - ${imgs.length}</div><button onclick="clearAllImages()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px">Anni Delete</button><div class="gallery">`;if(imgs.length==0)html+='<p style="color:#888">No images</p>';imgs.forEach((s,i)=>{html+=`<div style="position:relative"><img src="${s}"><button class="del-btn" onclick="deleteImage(${i})">✕</button></div>`});html+=`</div><br><button onclick="goHome()" style="background:#333;color:#fff;border:none;padding:8px 14px;border-radius:8px">← Back to Chat</button>`;mainDiv.innerHTML=html;}
function deleteImage(i){let a=JSON.parse(localStorage.getItem('ai_images')||'[]');a.splice(i,1);localStorage.setItem('ai_images',JSON.stringify(a));showImages();}
function clearAllImages(){if(confirm('Delete all?')){localStorage.removeItem('ai_images');showImages();}}
function showLibrary(){toggleMenu();let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');let html=`<div class="q-label">LIBRARY - ${chats.length}</div><button onclick="clearAllChats()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:8px;margin-bottom:10px">Anni Delete</button>`;if(chats.length==0)html+='<p style="color:#888">No chats</p>';chats.slice().reverse().forEach(c=>{html+=`<div class="card"><b>You:</b> ${c.q}<br><span style="color:#aaa">${c.a.substring(0,100)}</span></div>`});html+=`<br><button onclick="goHome()" style="background:#333;color:#fff;border:none;padding:8px 14px;border-radius:8px">← Back to Chat</button>`;mainDiv.innerHTML=html;}
function clearAllChats(){if(confirm('Delete all chats?')){localStorage.removeItem('ai_chats');localStorage.removeItem('ai_current');renderCurrentChat();}}
function clearAllData(){if(confirm('Motham delete cheyala?')){localStorage.clear();renderCurrentChat();toggleMenu();}}
function quick(t){inp.value=t;send();}
function startVoice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){alert('Chrome lo try chey');return;}let rec=new SR();rec.lang='te-IN';micBtn.classList.add('active');rec.onresult=e=>{inp.value=e.results[0][0].transcript;micBtn.classList.remove('active');send();};rec.onerror=()=>micBtn.classList.remove('active');rec.onend=()=>micBtn.classList.remove('active');rec.start();}
function speakText(t){if('speechSynthesis' in window){speechSynthesis.cancel();let u=new SpeechSynthesisUtterance(t);u.lang='te-IN';u.rate=0.9;speechSynthesis.speak(u);}}
async function send(){
 let t=inp.value.trim();if(!t)return;if(mainDiv.innerHTML.includes('LIBRARY')||mainDiv.innerHTML.includes('IMAGES'))renderCurrentChat();
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div><div id="typing" class="msg ai">♻️ Typing...</div>`;inp.value='';chatDiv.scrollTop=chatDiv.scrollHeight;
 try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();let ty=document.getElementById('typing');if(ty)ty.remove();mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply} <span style="cursor:pointer;color:#4a9eff" onclick="speakText('${d.reply.replace(/'/g,'')}')"><i class="fa-solid fa-volume-high"></i></span></div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');chats.push({q:t,a:d.reply});localStorage.setItem('ai_chats',JSON.stringify(chats));}catch(e){let ty=document.getElementById('typing');if(ty)ty.remove();mainDiv.innerHTML+=`<div class="msg ai">Network error</div>`;}chatDiv.scrollTop=chatDiv.scrollHeight;
}
async function scanImage(e){
 let file=e.target.files[0];if(!file)return;let b64=await new Promise(res=>{let img=new Image(),rd=new FileReader();rd.onload=ev=>{img.onload=()=>{let c=document.createElement('canvas'),max=600,w=img.width,h=img.height;if(w>h){if(w>max){h=h*max/w;w=max}}else{if(h>max){w=w*max/h;h=max}}c.width=w;c.height=h;c.getContext('2d').drawImage(img,0,0,w,h);res(c.toDataURL('image/jpeg',0.6).split(',')[1]);};img.src=ev.target.result;};rd.readAsDataURL(file);});
 let preview=`data:image/jpeg;base64,${b64}`;mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user"><img src="${preview}" style="max-width:200px;border-radius:12px"><br>Scanning...</div><div id="typing" class="msg ai">♻️ Scanning...</div>`;chatDiv.scrollTop=chatDiv.scrollHeight;
 try{let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});let d=await r.json();let ty=document.getElementById('typing');if(ty)ty.remove();mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">♻️ ${d.reply}</div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:'Image scan',a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');imgs.push(preview);localStorage.setItem('ai_images',JSON.stringify(imgs.slice(-20)));}catch(err){let ty=document.getElementById('typing');if(ty)ty.remove();mainDiv.innerHTML+=`<div class="msg ai">❌ ${err}</div>`;}chatDiv.scrollTop=chatDiv.scrollHeight;
}
</script></body></html>
"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg = request.json.get("message","")
    low = msg.lower()
    if GROQ_API_KEY:
        for model in ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]:
            try:
                r=requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
                json={"model":model,"messages":[{"role":"system","content":"You are Andhariki AI, Telugu+English recycling expert. Helpful, respectful."},{"role":"user","content":msg}],"max_tokens":800},timeout=12)
                j=r.json()
                if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except: continue
    if any(x in low for x in ["recycl","రిసైక్లింగ్","రీసైక్లింగ్","చెప్పు","plastic","paper","waste"]):
        return jsonify({"reply":"♻️ **Recycling Tips** 🌱\\n\\n🔵 **Plastic - Blue bin:** Bottles, covers - kadi aarabetti vey\\n🟢 **Paper - Green bin:** Books, papers - thadi kaadu\\n🟡 **Glass/Metal - Yellow bin:** Bottles, cans\\n🔴 **E-Waste - Red bin:** Battery, mobile, wires\\n\\n✨ **Golden Rule:** Reduce ➡️ Reuse ➡️ Recycle"})
    return jsonify({"reply": f"♻️ Hi babooie! '{msg}' gurinchi chepta! Recycling, waste - edaina adugu!"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img = request.json.get("image","")
        if not img:
            return jsonify({"reply":"📸 Image raaledu babooie"})

        prompt_text = """You are Andhariki AI, respectful Telugu+English assistant.
        Analyze the image carefully:
        - If it's a HUMAN PERSON (student, girl, boy, man, woman): Say in Telugu mix 'Idi manishi photo raa babooie 🙏 Oka vyakthi/student. Manushulu living beings, vaallani recycle cheyamu, gauravinchaali ❤️ Meeru waste gurinchi adagali anukunte plastic, paper, e-waste photos pettandi.' Be very respectful, NEVER call a person animal or item.
        - If it's ANIMAL/BIRD/PET: Say 'Idi [animal name] raa, living thing, recycle kaadu, protect cheyali ❤️' + 1 fun fact
        - If it's WASTE/OBJECT: Tell what it is, recyclable, which bin (Blue/Green/Yellow/Red), how to recycle.
        Answer short, respectful, Telugu+English mix with emojis.
        """

        # TRY GROQ VISION
        if GROQ_API_KEY:
            for m in ["llama-3.2-11b-vision-preview", "meta-llama/llama-4-scout-17b-16e-instruct", "llama-3.2-90b-vision-preview"]:
                try:
                    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
                        json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt_text},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":700},timeout=25)
                    j = r.json()
                    if "choices" in j and j["choices"]:
                        return jsonify({"reply": j["choices"][0]["message"]["content"]})
                except: continue

        # TRY GEMINI - BEST
        if GEMINI_API_KEY:
            for mn in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{mn}:generateContent?key={GEMINI_API_KEY}"
                    r = requests.post(url, json={"contents":[{"parts":[{"text":prompt_text},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]}, timeout=25)
                    j = r.json()
                    if "candidates" in j and j["candidates"]:
                        return jsonify({"reply": j["candidates"][0]["content"]["parts"][0]["text"]})
                except: continue

        # RESPECTFUL FALLBACK - NEVER CALL PERSON ANIMAL
        return jsonify({"reply": """🙏 **Idi manishi photo la undi babooie!**

Manushulu, students, animals, birds - veellu living beings ❤️ Vaallani manam recycle cheyamu, gauravinchaali, protect cheyali!

**Recycling kosam:**
🔵 Plastic/bottle -> Blue bin
🟢 Paper/books -> Green bin
🟡 Glass/metal -> Yellow bin
🔴 E-waste -> Red bin

Waste item photo pedithe adi ela recycle cheyalo chepta! 😊"""})

    except Exception as e:
        return jsonify({"reply": f"🙏 Photo chusa babooie! Manishi ayite gauravam, waste ayite recycling. Malli try chey! {str(e)[:50]}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
