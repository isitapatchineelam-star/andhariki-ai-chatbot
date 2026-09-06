from flask import Flask, request, jsonify
import os, requests, re
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
.mic-btn{width:32px;height:32px;display:flex;align-items:center;justify-content:center;color:#9e9e9e;cursor:pointer;font-size:18px}
.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer;flex-shrink:0}
#fileInput{display:none}.toast{position:fixed;top:70px;left:50%;transform:translateX(-50%);background:#fff;color:#000;padding:10px 20px;border-radius:20px;z-index:100;display:none}
</style></head><body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div><div class="toast" id="toast"></div>
<div class="sidebar" id="sidebar">
<div style="padding:0 20px 20px;border-bottom:1px solid #2a2a2a"><b>♻️ Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()">+ New chat</div>
<div class="side-item" onclick="goHome()"><i class="fa-solid fa-house"></i> Home</div>
<div class="side-item" onclick="clearAllData()"><i class="fa-solid fa-trash"></i> Clear All</div>
</div>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="menu" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i></div><b>Andhariki AI</b></div><div class="menu" onclick="newChat()"><i class="fa-solid fa-pen-to-square"></i></div></div>
<div class="chat" id="chat"><div id="mainContent"></div></div>
<div class="input-area"><div class="input-box">
<div style="color:#8e8ea0;cursor:pointer" onclick="document.getElementById('fileInput').click()"><i class="fa-solid fa-plus"></i></div>
<input id="inp" placeholder="Ask anything - Yee question ki answer vastadi..." onkeypress="if(event.key==='Enter')send()">
<input type="file" id="fileInput" accept="image/*" onchange="scanImage(event)">
<div class="mic-btn" id="micBtn" onclick="startVoice()"><i class="fa-solid fa-microphone"></i></div>
<div class="voice-circle" onclick="send()"><i class="fa-solid fa-arrow-up"></i></div>
</div></div>
<script>
const mainDiv=document.getElementById('mainContent'),chatDiv=document.getElementById('chat'),inp=document.getElementById('inp');
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function goHome(){document.getElementById('sidebar').classList.remove('open');document.getElementById('overlay').classList.remove('show');renderCurrentChat();}
function renderCurrentChat(){
  let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');mainDiv.innerHTML='';
  if(cur.length==0){mainDiv.innerHTML=`<div style="margin:20% 0;text-align:center;color:#8e8ea0"><b style="color:#fff">Yee question ki REAL answer vastadi! ✅</b><br><br><div style="text-align:left;max-width:320px;margin:auto;line-height:2.8"><div onclick="quick('what is ai?')" style="cursor:pointer">🤖 what is ai?</div><div onclick="quick('photosynthesis definition evvu')" style="cursor:pointer">🌱 photosynthesis definition</div><div onclick="quick('x=4 print x?')" style="cursor:pointer">💻 x=4 print x?</div><div onclick="quick('python ante enti')" style="cursor:pointer">🐍 python ante enti</div><div onclick="quick('how to impress my friend')" style="cursor:pointer">❤️ how to impress my friend</div></div></div>`;}
  else{cur.forEach(c=>{mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${c.q}</div><div class="q-label">Andhariki AI</div><div class="msg ai">${c.a}</div>`;});}
  chatDiv.scrollTop=chatDiv.scrollHeight;
}
window.onload=renderCurrentChat;
function newChat(){localStorage.removeItem('ai_current');renderCurrentChat();}
function clearAllData(){if(confirm('Clear?')){localStorage.clear();renderCurrentChat();toggleMenu();}}
function quick(t){inp.value=t;send();}
function startVoice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){alert('Chrome lo try chey');return;}let rec=new SR();rec.lang='te-IN';rec.onresult=e=>{inp.value=e.results[0][0].transcript;send();};rec.start();}
async function send(){
 let t=inp.value.trim();if(!t)return;
 if(mainDiv.innerHTML.includes('Yee question')){mainDiv.innerHTML='';}
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div><div id="typing" class="msg ai">Thinking...</div>`;inp.value='';chatDiv.scrollTop=chatDiv.scrollHeight;
 try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();document.getElementById('typing')?.remove();mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));}catch(e){document.getElementById('typing')?.remove();mainDiv.innerHTML+=`<div class="msg ai">Network error, try again</div>`;}chatDiv.scrollTop=chatDiv.scrollHeight;
}
async function scanImage(e){
 let file=e.target.files[0];if(!file)return;let b64=await new Promise(res=>{let rd=new FileReader();rd.onload=ev=>res(ev.target.result.split(',')[1]);rd.readAsDataURL(file);});
 mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user"><img src="data:image/jpeg;base64,${b64}" style="max-width:200px;border-radius:12px"></div><div id="typing" class="msg ai">Scanning...</div>`;chatDiv.scrollTop=chatDiv.scrollHeight;
 try{let r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});let d=await r.json();document.getElementById('typing')?.remove();mainDiv.innerHTML+=`<div class="q-label">Andhariki AI</div><div class="msg ai">${d.reply}</div>`;}catch{let ty=document.getElementById('typing');if(ty)ty.remove();}
}
</script></body></html>
"""

def get_wiki(q):
    try:
        q = q.replace("definition","").replace("evvu","").replace("ante enti","").replace("?","").strip()
        if len(q)<2: return None
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ','_')}", timeout=4, headers={"User-Agent":"AndharikiAI"})
        j=r.json()
        if "extract" in j and len(j["extract"])>20:
            return j["extract"]
    except: pass
    return None

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.json
    msg = data.get("message","").strip()
    low = msg.lower()

    # 1. TRY GROQ / GEMINI FOR ANY QUESTION
    if GROQ_API_KEY:
        for model in ["llama-3.1-8b-instant","llama-3.3-70b-versatile"]:
            try:
                r=requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ_API_KEY}"},
                json={"model":model,"messages":[{"role":"system","content":"You are Andhariki AI. Answer ANY question in detail, in Telugu+English mix. Be helpful."},{"role":"user","content":msg}],"max_tokens":1000},timeout=10)
                j=r.json()
                if "choices" in j and len(j["choices"])>0:
                    return jsonify({"reply":j["choices"][0]["message"]["content"]})
            except: continue

    if GEMINI_API_KEY:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r=requests.post(url,json={"contents":[{"parts":[{"text":f"Answer this in Telugu mix, detailed: {msg}"}]}]},timeout=10)
            j=r.json()
            if "candidates" in j:
                return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass

    # 2. NO KEY? STILL GIVE REAL ANSWER VIA WIKIPEDIA + LOGIC
    # Code
    m=re.search(r'x\s*=\s*(\d+)',low)
    if "print" in low and m:
        return jsonify({"reply":f"💻 **Answer: {m.group(1)}**\n\n```python\nx = {m.group(1)}\nprint(x)\n```\nOutput: **{m.group(1)}** ✅"})

    # Math
    if re.match(r'^[\d\+\-\*\/\(\)\s]+$', msg) and len(msg)<15:
        try:
            ans=eval(msg,{"__builtins__":None},{})
            return jsonify({"reply":f"🔢 **Answer: {ans}** ✅\n`{msg} = {ans}`"})
        except: pass

    # Direct big answers
    if "ai" in low and len(low)<30:
        return jsonify({"reply":"🤖 **AI - Artificial Intelligence:**\n\nAI ante computer ki manishi laga alochinche shakti ivvadam.\n\n**Ex:** ChatGPT, Google Assistant\n**Types:** Narrow AI, General AI, Super AI\n**Uses:** Medical, Education, Business anni chotla\n\nSimple ga: Machine ki brain pettadam = AI 😊"})
    if "python" in low:
        return jsonify({"reply":"🐍 **Python:** Chala easy programming language (1991). Instagram, YouTube kuda Python tho chesaru!\n\n```python\nx=5\nprint(x) # 5\n```\nEasy, powerful!"})
    if "photosynthesis" in low:
        return jsonify({"reply":"🌱 **Photosynthesis:** Mokalu sunlight + water + CO2 tho food + oxygen chese process.\n\nFormula: 6CO2+6H2O+Light → C6H12O6+6O2"})
    if "black hole" in low:
        return jsonify({"reply":"🌌 **Black Hole:** Gravity chala ekkuva unna space region, light kuda escape avadu. Pedda star chanipote vastundi."})
    if "friend" in low or "impress" in low:
        return jsonify({"reply":"❤️ **Friend impress:**\n1. Nijam ga undu\n2. Baga vinu\n3. Help chey\n4. Small surprise\nGenuine friendship chalu! 😊"})

    if low.strip() in ["definition evvu","definition"]:
        return jsonify({"reply":"📚 **Topic cheppu babooie!**\n\n`definition evvu` ani matrame annav.\n\nIla adugu:\n• AI definition evvu\n• Photosynthesis definition\n• Python ante enti\n\nFull answer ista!"})

    # Wikipedia for ANY TOPIC
    clean = re.sub(r'definition|evvu|ante enti|what is|meaning|\?','',low).strip()
    if len(clean)>=2:
        w=get_wiki(clean)
        if w:
            return jsonify({"reply":f"📚 **{clean.title()} - Definition:**\n\n{w}\n\n✅ Source: Wikipedia"})

    # Final fallback - NOT recycling only!
    return jsonify({"reply":f"😊 **{msg} gurinchi:**\n\nNenu Wikipedia lo chusanu. '{clean if clean else msg}' gurinchi info:\n\n{get_wiki(clean) or 'Idi chala interesting topic! Konchem clear ga adugu babooie - ex: `'+msg+' ante enti` - nenu full details tho answer ista! 😊'}"})

@app.route("/scan", methods=["POST"])
def scan():
    try:
        img = request.json.get("image","")
        if not img: return jsonify({"reply":"Image raaledu"})
        prompt_text = "If HUMAN: say 'Manishi photo 🙏 gauravinchaali'. If animal: protect cheyali. If waste: what bin, how recycle. If other: describe what you see. Telugu+English mix."
        if GROQ_API_KEY:
            for m in ["meta-llama/llama-4-scout-17b-16e-instruct","llama-3.2-11b-vision-preview"]:
                try:
                    r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_API_KEY}"},
                    json={"model":m,"messages":[{"role":"user","content":[{"type":"text","text":prompt_text},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}]},timeout=20)
                    j=r.json()
                    if "choices" in j: return jsonify({"reply":j["choices"][0]["message"]["content"]})
                except: continue
        if GEMINI_API_KEY:
            try:
                url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                r=requests.post(url,json={"contents":[{"parts":[{"text":prompt_text},{"inline_data":{"mime_type":"image/jpeg","data":img}}]}]},timeout=20)
                j=r.json()
                if "candidates" in j: return jsonify({"reply":j["candidates"][0]["content"]["parts"][0]["text"]})
            except: pass
        return jsonify({"reply":"📸 Photo chusa! Manishi/animal ayite protect cheyali ❤️ Waste ayite recycle chey! 😊"})
    except Exception as e:
        return jsonify({"reply":f"Photo chusa! {str(e)[:50]}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
