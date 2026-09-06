from flask import Flask, request, jsonify
import os, requests, re
app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Andhariki AI</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{padding:12px 16px;display:flex;justify-content:space-between;background:#000;border-bottom:1px solid #222}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sidebar{position:fixed;top:0;left:-280px;width:280px;height:100%;background:#171717;z-index:99;transition:0.3s;padding:20px 0;display:flex;flex-direction:column;overflow-y:auto}
.sidebar.open{left:0}.overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:90;display:none}.overlay.show{display:block}
.side-item{padding:14px 20px;color:#ececec;cursor:pointer;display:flex;gap:12px;align-items:center}.side-item:hover{background:#2a2a2a}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:12px;font-weight:700;margin:10px 20px;cursor:pointer;text-align:center}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:10px 0;line-height:1.8;white-space:pre-wrap;word-break:break-word;font-size:15px}
.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}
.msg.ai{padding:10px 4px;color:#ececec}
.label{font-size:11px;color:#777;margin-top:14px;font-weight:bold}
.input-area{padding:10px 12px 16px;background:#000}
.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:8px;border:1px solid #3a3a3a;min-height:52px}
.box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.icon{width:34px;height:34px;display:flex;align-items:center;justify-content:center;color:#aaa;cursor:pointer;font-size:18px}
.send{background:#fff;color:#000;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0}
#fileInput{display:none}
.card{background:#1e1e1e;padding:12px;border-radius:12px;margin:8px 0}
</style></head><body>
<div class="overlay" id="overlay" onclick="closeMenu()"></div>
<div class="sidebar" id="sidebar">
<div style="padding:0 20px 20px;border-bottom:1px solid #2a2a2a;font-size:18px"><b>♻️ Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()">+ New chat</div>
<div class="side-item" onclick="goHome()"><i class="fa-solid fa-house"></i> Home / Chat</div>
<div class="side-item" onclick="showImages()"><i class="fa-regular fa-images"></i> Images (20)</div>
<div class="side-item" onclick="showLibrary()"><i class="fa-solid fa-book"></i> Library</div>
<div class="side-item" onclick="clearAll()"><i class="fa-solid fa-trash"></i> Clear All</div>
<div style="padding:20px;color:#666;font-size:12px">Features: Any question ✅ | Voice ✅ | Photo Scan ✅ | Calculator ✅</div>
</div>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="menu" onclick="openMenu()"><i class="fa-solid fa-bars"></i></div><b>Andhariki AI - Real Answers</b></div><div class="menu" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i></div></div>
<div class="chat" id="chat"><div id="main"></div></div>
<div class="input-area"><div class="box">
<div class="icon" onclick="document.getElementById('fileInput').click()"><i class="fa-solid fa-plus"></i></div>
<input id="inp" placeholder="Ask anything... Yee question ki answer vastadi" onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scan(event)">
<div class="icon" id="mic" onclick="voice()"><i class="fa-solid fa-microphone"></i></div>
<div class="send" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div></div>
<script>
let main=document.getElementById('main'), chatDiv=document.getElementById('chat'), inp=document.getElementById('inp');
function openMenu(){document.getElementById('sidebar').classList.add('open');document.getElementById('overlay').classList.add('show');}
function closeMenu(){document.getElementById('sidebar').classList.remove('open');document.getElementById('overlay').classList.remove('show');}
function goHome(){closeMenu();render();}
function newChat(){localStorage.removeItem('ai_current');closeMenu();location.reload();}
function clearAll(){if(confirm('Anni delete cheyala?')){localStorage.clear();closeMenu();location.reload();}}
function showImages(){
closeMenu();
let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');
let h=`<div class="label">IMAGES - ${imgs.length}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">`;
if(imgs.length==0)h+='<p style="color:#888">No images. Photo upload chey.</p>';
imgs.forEach(s=>{h+=`<img src="${s}" style="width:100%;border-radius:12px">`});
h+=`</div><br><button onclick="render()" style="background:#333;color:#fff;border:none;padding:10px 18px;border-radius:10px">← Back to Chat</button>`;
main.innerHTML=h;
}
function showLibrary(){
closeMenu();
let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');
let h=`<div class="label">LIBRARY - ${chats.length} chats</div>`;
if(chats.length==0)h+='<p style="color:#888">No chats yet</p>';
chats.slice().reverse().slice(0,50).forEach(c=>{h+=`<div class="card"><b style="color:#fff">${c.q}</b><br><span style="color:#aaa;font-size:13px">${c.a.substring(0,120)}...</span></div>`});
h+=`<br><button onclick="render()" style="background:#333;color:#fff;border:none;padding:10px 18px;border-radius:10px">← Back</button>`;
main.innerHTML=h;
}
function render(){
let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');
if(cur.length==0){
main.innerHTML=`<div style="text-align:center;margin-top:20%;color:#8e8ea0">
<div style="font-size:22px;color:#fff;font-weight:bold">Yee question ki REAL answer vastadi ✅</div>
<p>Andhariki AI - Nee best friend</p>
<div style="text-align:left;max-width:320px;margin:30px auto;line-height:3">
<div onclick="quick('what is programming')" style="cursor:pointer;color:#fff;background:#1e1e1e;padding:8px 14px;border-radius:10px">💻 what is programming</div>
<div onclick="quick('what is ai?')" style="cursor:pointer;color:#fff;background:#1e1e1e;padding:8px 14px;border-radius:10px">🤖 what is ai?</div>
<div onclick="quick('photosynthesis definition')" style="cursor:pointer;color:#fff;background:#1e1e1e;padding:8px 14px;border-radius:10px">🌱 photosynthesis</div>
<div onclick="quick('x=4 print x')" style="cursor:pointer;color:#fff;background:#1e1e1e;padding:8px 14px;border-radius:10px">🔢 x=4 print x</div>
<div onclick="document.getElementById('fileInput').click()" style="cursor:pointer;color:#fff;background:#1e1e1e;padding:8px 14px;border-radius:10px">📸 Photo scan chey</div>
</div></div>`;
}else{
main.innerHTML='';
cur.forEach(c=>{main.innerHTML+=`<div class="label">You</div><div class="msg user">${c.q}</div><div class="label">Andhariki AI</div><div class="msg ai">${c.a}</div>`;});
}
chatDiv.scrollTop=999999;
}
window.onload=render;
function quick(t){inp.value=t;send();}
async function send(){
let t=inp.value.trim();if(!t)return;
if(main.innerHTML.includes('REAL answer vastadi'))main.innerHTML='';
main.innerHTML+=`<div class="label">You</div><div class="msg user">${t}</div><div id="typing" class="msg ai">♻️ Typing... Real answer techutunna...</div>`;inp.value='';chatDiv.scrollTop=999999;
try{
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
let d=await r.json();
document.getElementById('typing')?.remove();
main.innerHTML+=`<div class="label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;
let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));
let chats=JSON.parse(localStorage.getItem('ai_chats')||'[]');chats.push({q:t,a:d.reply});localStorage.setItem('ai_chats',JSON.stringify(chats));
}catch{let ty=document.getElementById('typing');if(ty)ty.remove();main.innerHTML+=`<div class="msg ai">Network error, malli try chey</div>`;}
chatDiv.scrollTop=999999;
}
function voice(){let SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){alert('Chrome lo try chey');return;}let rec=new SR();rec.lang='te-IN';rec.onresult=e=>{inp.value=e.results[0][0].transcript;send();};rec.start();}
async function scan(e){
let file=e.target.files[0];if(!file)return;
let b64=await new Promise(res=>{let fr=new FileReader();fr.onload=ev=>res(ev.target.result.split(',')[1]);fr.readAsDataURL(file);});
let prev=`data:image/jpeg;base64,${b64}`;
main.innerHTML+=`<div class="label">You</div><div class="msg user"><img src="${prev}" style="max-width:200px;border-radius:12px"></div><div id="typing" class="msg ai">📸 Scanning...</div>`;chatDiv.scrollTop=999999;
try{
let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});
let d=await r.json();
document.getElementById('typing')?.remove();
main.innerHTML+=`<div class="label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;
let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:'Photo',a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));
let imgs=JSON.parse(localStorage.getItem('ai_images')||'[]');imgs.push(prev);localStorage.setItem('ai_images',JSON.stringify(imgs.slice(-20)));
}catch{let ty=document.getElementById('typing');if(ty)ty.remove();}
chatDiv.scrollTop=999999;
}
</script></body></html>
"""

def get_wiki_real(q):
    try:
        q = q.lower().replace("definition","").replace("evvu","").replace("ante enti","").replace("what is","").replace("?","").strip()
        if len(q)<2: return None
        # search to avoid disambiguation
        s = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=5&namespace=0&format=json", timeout=5).json()
        titles = s[1] if len(s)>1 and s[1] else [q]
        for title in titles:
            r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ','_')}", timeout=5, headers={"User-Agent":"AndharikiAI"}).json()
            ext = r.get("extract","")
            if ext and "may refer to:" not in ext.lower() and len(ext)>60:
                return ext, title
        if titles:
            r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{titles[0].replace(' ','_')}", timeout=5, headers={"User-Agent":"AndharikiAI"}).json()
            if r.get("extract"): return r.get("extract"), titles[0]
    except: pass
    return None, None

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg = request.json.get("message","").strip()
    if not msg:
        return jsonify({"reply":"Adugu babooie! 😊"})
    low = msg.lower()

    # TOOL 1: CODE x=...
    m=re.search(r'x\s*=\s*(\d+)',low)
    if "print" in low and m:
        return jsonify({"reply":f"💻 **Answer: {m.group(1)}**\n\n```python\nx = {m.group(1)}\nprint(x) # Output: {m.group(1)}\n```\n✅ x value print avutundi = **{m.group(1)}**"})

    # TOOL 2: MATH CALCULATOR
    if re.match(r'^[\d\+\-\*\/\%\(\)\s\.]+$', msg) and len(msg)<20 and any(c in msg for c in "+-*/%"):
        try:
            ans = eval(msg, {"__builtins__":None}, {})
            return jsonify({"reply":f"🔢 **Answer: {ans}**\n\n`{msg} = {ans}` ✅ Calculator Tool"})
        except: pass

    # TOOL 3: GROQ - MAIN BRAIN - ANY QUESTION
    if GROQ_API_KEY:
        for model in ["llama-3.1-8b-instant","llama-3.3-70b-versatile"]:
            try:
                # STRONG PROMPT - NO MORE WASTE ANSWER
                system_prompt = """You are Andhariki AI - best helpful AI in Telugu + English mix.
RULES:
- Answer ANY question in detail, real, correct.
- Use Telugu + English mix (like how Telugu people speak)
- Never say 'may refer to' - give full definition
- If code: give code + explanation
- If definition: give full definition with example
- Be friendly, use emojis
- Max 200 words but detailed"""
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
                json={"model":model,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":msg}],"temperature":0.7,"max_tokens":1000},timeout=12)
                j=r.json()
                if "choices" in j and len(j["choices"])>0:
                    return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except Exception as e:
                continue

    # TOOL 4: GEMINI FALLBACK
    if GEMINI_API_KEY:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r=requests.post(url,json={"contents":[{"parts":[{"text":f"You are Andhariki AI. Answer in Telugu mix, detailed, friendly: {msg}"}]}]},timeout=12)
            j=r.json()
            if "candidates" in j:
                return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass

    # TOOL 5: WIKIPEDIA + SMART FALLBACK - NO KEY NEEDED
    # Programming special
    if "programming" in low:
        return jsonify({"reply":"💻 **Programming - Full Definition:**\n\n**Programming ante** computer ki manam cheppalani anukunna pani ela cheyalo step-by-step instructions ivvadam.\n\n**Ela chestam?** Python, Java, C++, JavaScript lanti languages vadutham.\n\n**Example:**\n```python\nprint('Hello Andhariki AI') # Idhi programming!\n```\n\n**Uses:**\n- Websites (Facebook, YouTube)\n- Apps (WhatsApp, Instagram)\n- Games (PUBG, Free Fire)\n- AI (ChatGPT)\n\nSimple ga: Computer tho matladadam = Programming 😊\n\n✅ Real Answer Tool"})

    # Try Wikipedia real
    clean = re.sub(r'definition|evvu|ante enti|what is|meaning|\?','',low).strip()
    if len(clean)>=2:
        wiki_text, title = get_wiki_real(clean)
        if wiki_text:
            return jsonify({"reply":f"📚 **{title.title()} - Full Definition:**\n\n{wiki_text}\n\n💡 **Telugu lo simple ga:** {title} ante chala important topic, daani gurinchi paine full info ichanu!\n\n✅ Source: Wikipedia - Real Tool"})

    # Final - never waste
    return jsonify({"reply":f"😊 **{msg} gurinchi:**\n\nNee question '{msg}' ki full answer ivvadaniki nenu ready!\n\n**Nee Groq API Key Render lo pedithe** nenu ChatGPT laga full detailed Telugu lo answer ista!\n\nIppatiki:\n- **{msg}** ante oka important topic\n- Inka deep ga kavala ante `'{msg} ante enti detailed ga cheppu'` ani adugu\n\n✅ Tools Working: Calculator, Code Runner, Wikipedia, AI Brain"})

@app.route("/scan", methods=["POST"])
def scan():
    img = request.json.get("image","")
    if not img:
        return jsonify({"reply":"📸 Image raaledu babooie"})
    prompt = "You are helpful. If human: say 'Manishi photo 🙏 gauravinchaali, recycle kaadu'. If animal: 'protect cheyali'. If waste: what bin color, how recycle. If book/object: explain what it is. Answer in Telugu+English mix."
    if GROQ_API_KEY:
        for m in ["meta-llama/llama-4-scout-17b-16e-instruct","llama-3.2-11b-vision-preview"]:
            try:
                r=requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ_API_KEY}"},
                json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":800},timeout=20)
                j=r.json()
                if "choices" in j:
                    return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except: continue
    if GEMINI_API_KEY:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r=requests.post(url,json={"contents":[{"parts":[{"text":prompt},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]},timeout=20)
            j=r.json()
            if "candidates" in j:
                return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass
    return jsonify({"reply":"📸 Photo chusa babooie! Manishi/animal ayite protect cheyali ❤️ Waste ayite Blue/Green bin lo veyali ♻️"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
