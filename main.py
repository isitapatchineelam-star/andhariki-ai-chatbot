from flask import Flask, request, jsonify
import os, requests, re
app = Flask(__name__)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_PAGE = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Andhariki AI</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{padding:10px 12px;display:flex;justify-content:space-between;background:#000;border-bottom:1px solid #222;align-items:center}
.menu{width:32px;height:32px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
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
.voice-circle{width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#000;cursor:pointer}
</style></head><body>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>
<div class="sidebar" id="sidebar"><div style="padding:0 20px 20px;border-bottom:1px solid #2a2a2a"><b>Andhariki AI</b></div>
<div class="new-chat" onclick="newChat()">+ New chat</div>
<div class="side-item" onclick="goHome()">🏠 Home</div>
<div class="side-item" onclick="clearAll()">🗑️ Clear</div></div>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div class="menu" onclick="toggleMenu()">☰</div><b>Andhariki AI</b></div><div class="menu" onclick="newChat()">✎</div></div>
<div class="chat" id="chat"><div id="mainContent"></div></div>
<div class="input-area"><div class="input-box">
<input id="inp" placeholder="Yee question adigina answer vastadi..." onkeypress="if(event.key==='Enter')send()">
<div class="voice-circle" onclick="send()">↑</div>
</div></div>
<script>
const mainDiv=document.getElementById('mainContent'),chatDiv=document.getElementById('chat'),inp=document.getElementById('inp');
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function goHome(){document.getElementById('sidebar').classList.remove('open');document.getElementById('overlay').classList.remove('show');render();}
function render(){let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');mainDiv.innerHTML='';if(cur.length==0){mainDiv.innerHTML=`<div style="margin:30% 0;text-align:center;color:#8e8ea0"><b style="color:#fff">Yee question ki REAL answer vastadi! ✅</b><br><br><div style="text-align:left;max-width:300px;margin:auto;line-height:2.5"><div onclick="quick('photosynthesis definition evvu')">📚 photosynthesis definition</div><div onclick="quick('x=4 then print x')">💻 x=4 then print x</div><div onclick="quick('what is black hole?')">🌌 what is black hole?</div><div onclick="quick('how to impress my friend')">❤️ how to impress my friend</div><div onclick="quick('definition evvu')">📖 definition evvu</div></div></div>`;}else{cur.forEach(c=>{mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${c.q}</div><div class="q-label">AI</div><div class="msg ai">${c.a}</div>`;});}chatDiv.scrollTop=chatDiv.scrollHeight;}
window.onload=render;
function newChat(){localStorage.removeItem('ai_current');render();}
function clearAll(){if(confirm('Clear?')){localStorage.clear();render();toggleMenu();}}
function quick(t){inp.value=t;send();}
async function send(){let t=inp.value.trim();if(!t)return;if(mainDiv.innerHTML.includes('Yee question')){mainDiv.innerHTML='';}mainDiv.innerHTML+=`<div class="q-label">You</div><div class="msg user">${t}</div><div id="typing" class="msg ai">Thinking...</div>`;inp.value='';chatDiv.scrollTop=chatDiv.scrollHeight;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();document.getElementById('typing')?.remove();mainDiv.innerHTML+=`<div class="q-label">AI</div><div class="msg ai">${d.reply}</div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));}catch(e){document.getElementById('typing')?.remove();mainDiv.innerHTML+=`<div class="msg ai">Error</div>`;}chatDiv.scrollTop=chatDiv.scrollHeight;}
</script></body></html>
"""

def get_wiki(topic):
    try:
        topic = topic.replace("definition","").replace("evvu","").replace("ante enti","").replace("what is","").replace("?","").strip()
        if len(topic)<2: return None
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}",timeout=5,headers={"User-Agent":"AndharikiAI"})
        j=r.json()
        if "extract" in j: return j["extract"]
    except: pass
    return None

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg=request.json.get("message","").strip()
    low=msg.lower()

    # API keys try
    for k in [os.environ.get("GROQ_API_KEY"), os.environ.get("GROQ_API_KEY2")]:
        if not k: continue
        try:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {k}"},json={"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":msg}]},timeout=5)
            if "choices" in r.json(): return jsonify({"reply":r.json()["choices"][0]["message"]["content"]})
        except: pass
    if GEMINI_API_KEY:
        try:
            u=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r=requests.post(u,json={"contents":[{"parts":[{"text":msg}]}]},timeout=5)
            if "candidates" in r.json(): return jsonify({"reply":r.json()["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass

    # CODE x=4
    m=re.search(r'x\s*=\s*(\d+)',low)
    if "print" in low and m: return jsonify({"reply":f"💻 **Answer: {m.group(1)}**\n```python\nx = {m.group(1)}\nprint(x)\n```\nOutput: {m.group(1)} ✅"})

    # MATH
    if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', msg) and len(msg)<15:
        try: return jsonify({"reply":f"🔢 Answer: {eval(msg,{'__builtins__':None},{})} ✅"})
        except: pass

    # only "definition evvu"
    if low.strip() in ["definition evvu","definition"] or len(low.split())<=2 and "definition" in low:
        return jsonify({"reply":"📚 **Topic cheppu babooie!**\n\n`definition evvu` ani matrame annav.\n\nIla adugu:\n• photosynthesis definition evvu\n• black hole definition\n• recycling definition\n\nREAL answer Wikipedia nundi ista! 😊"})

    # WIKIPEDIA REAL
    clean=msg
    for w in ["definition evvu","definition","ante enti","what is","meaning"]: clean=clean.lower().replace(w,"")
    clean=clean.strip()
    if len(clean)>=2:
        wiki=get_wiki(clean)
        if wiki: return jsonify({"reply":f"📚 **{clean.title()} - Definition:**\n\n{wiki}\n\n✅ Wikipedia"})

    if "friend" in low: return jsonify({"reply":"❤️ **Friend impress:** Nijam ga undu, baga vinu, help chey, small surprise ivvu 😊"})
    if "black hole" in low: return jsonify({"reply":"🌌 **Black Hole:** Chala ekkuva gravity unna space place, light kuda escape avadu."})
    if "photosynthesis" in low: return jsonify({"reply":"🌱 **Photosynthesis:** Plants sunlight tho food chestayi. 6CO2+6H2O+Light→C6H12O6+6O2"})

    return jsonify({"reply":f"📚 **{msg}** gurinchi konchem clear ga topic tho adugu babooie - ex: `{msg} definition` - REAL answer ista! 😊"})

@app.route("/scan", methods=["POST"])
def scan(): return jsonify({"reply":"📸 Photo chusa!"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
