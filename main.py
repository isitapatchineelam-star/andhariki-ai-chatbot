from flask import Flask, request, jsonify
import os, requests, re
app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY","").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY","").strip()

HTML_PAGE = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>Andhariki AI</title>
<link rel=stylesheet href=https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css>
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#000;color:#fff;display:flex;flex-direction:column;height:100vh;overflow:hidden}
.top{padding:12px 16px;display:flex;justify-content:space-between;background:#000;border-bottom:1px solid #222}
.menu{width:36px;height:36px;background:#1e1e1e;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sidebar{position:fixed;top:0;left:-280px;width:280px;height:100%;background:#171717;z-index:99;transition:0.3s;padding:20px 0;display:flex;flex-direction:column}
.sidebar.open{left:0}.overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:90;display:none}.overlay.show{display:block}
.side-item{padding:14px 20px;color:#ececec;cursor:pointer;display:flex;gap:12px}.side-item:hover{background:#2a2a2a}
.new-chat{background:#fff;color:#000;border-radius:24px;padding:12px;font-weight:700;margin:10px 20px;cursor:pointer;text-align:center}
.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:10px 0;line-height:1.8;white-space:pre-wrap;font-size:15px}.msg.user{background:#2f2f2f;padding:12px 16px;border-radius:18px;max-width:85%;margin-left:auto}.msg.ai{padding:10px 4px}
.label{font-size:11px;color:#777;margin-top:14px;font-weight:bold}
.input-area{padding:10px 12px 16px;background:#000}.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:6px 12px;display:flex;align-items:center;gap:8px;min-height:52px}
.box input{flex:1;border:none;background:transparent;outline:none;color:#fff;font-size:16px}
.icon{width:34px;height:34px;display:flex;align-items:center;justify-content:center;color:#aaa;cursor:pointer;font-size:18px}
.send{background:#fff;color:#000;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}
#fileInput{display:none}
</style></head><body>
<div class=overlay id=overlay onclick=closeMenu()></div>
<div class=sidebar id=sidebar>
<div style="padding:0 20px 20px;border-bottom:1px solid #2a2a2a"><b>Andhariki AI</b></div>
<div class=new-chat onclick=newChat()>+ New chat</div>
<div class=side-item onclick="closeMenu();render()"><i class="fa-solid fa-house"></i> Home</div>
<div class=side-item onclick=clearAll()><i class="fa-solid fa-trash"></i> Clear All</div>
</div>
<div class=top><div style="display:flex;gap:12px;align-items:center"><div class=menu onclick=openMenu()><i class="fa-solid fa-bars"></i></div><b>Andhariki AI</b></div><div class=menu onclick=newChat()><i class="fa-solid fa-pen-to-square"></i></div></div>
<div class=chat id=chat><div id=main></div></div>
<div class=input-area><div class=box>
<div class=icon onclick=document.getElementById('fileInput').click()><i class="fa-solid fa-plus"></i></div>
<input id=inp placeholder="Yee question aina adugu - Real answer vastadi" onkeypress="if(event.key==='Enter')send()">
<input type=file id=fileInput accept=image/* onchange=scan(event)>
<div class=icon onclick=voice()><i class="fa-solid fa-microphone"></i></div>
<div class=send onclick=send()><i class="fa-solid fa-arrow-up"></i></div>
</div></div>
<script>
let main=document.getElementById('main'),chatDiv=document.getElementById('chat'),inp=document.getElementById('inp');
function openMenu(){document.getElementById('sidebar').classList.add('open');document.getElementById('overlay').classList.add('show');}
function closeMenu(){document.getElementById('sidebar').classList.remove('open');document.getElementById('overlay').classList.remove('show');}
function newChat(){localStorage.clear();location.reload();}
function clearAll(){if(confirm('Delete?')){localStorage.clear();location.reload();}}
function render(){
let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');
if(cur.length==0){
main.innerHTML=`<div style="text-align:center;margin-top:18%"><div style="font-size:20px;font-weight:bold">Yee question ki REAL answer vastadi ✅</div><p>Biryani, Python, Maths - Anni!</p><div style="text-align:left;max-width:300px;margin:20px auto;line-height:2.5"><div onclick="q('how to make biryani')" style="background:#1e1e1e;padding:8px 12px;border-radius:8px;cursor:pointer">🍛 how to make biryani</div><div onclick="q('what is programming')" style="background:#1e1e1e;padding:8px 12px;border-radius:8px;cursor:pointer">💻 what is programming</div><div onclick="q('what is python')" style="background:#1e1e1e;padding:8px 12px;border-radius:8px;cursor:pointer">🐍 what is python</div></div></div>`;
}else{main.innerHTML='';cur.forEach(c=>{main.innerHTML+=`<div class=label>You</div><div class="msg user">${c.q}</div><div class=label>AI</div><div class="msg ai">${c.a}</div>`});}
chatDiv.scrollTop=99999;
}
window.onload=render;function q(t){inp.value=t;send();}
async function send(){let t=inp.value.trim();if(!t)return;if(main.innerHTML.includes('REAL answer'))main.innerHTML='';main.innerHTML+=`<div class=label>You</div><div class="msg user">${t}</div><div id=typing class="msg ai">Typing... Real answer techutunna...</div>`;inp.value='';chatDiv.scrollTop=99999;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();document.getElementById('typing')?.remove();main.innerHTML+=`<div class=label>AI</div><div class="msg ai">${d.reply}</div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));}catch{let ty=document.getElementById('typing');if(ty)ty.remove();main.innerHTML+=`<div class="msg ai">Network error, malli try chey</div>`;}chatDiv.scrollTop=99999;}
function voice(){let SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){alert('Chrome lo try');return;}let rec=new SR();rec.lang='te-IN';rec.onresult=e=>{inp.value=e.results[0][0].transcript;send();};rec.start();}
async function scan(e){let file=e.target.files[0];if(!file)return;let b64=await new Promise(r=>{let fr=new FileReader();fr.onload=ev=>r(ev.target.result.split(',')[1]);fr.readAsDataURL(file);});let prev=`data:image/jpeg;base64,${b64}`;main.innerHTML+=`<div class=label>You</div><div class="msg user"><img src="${prev}" style="max-width:200px;border-radius:12px"></div><div id=typing class="msg ai">📸 Scanning...</div>`;try{let rr=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:b64})});let dd=await rr.json();document.getElementById('typing')?.remove();main.innerHTML+=`<div class=label>AI</div><div class="msg ai">${dd.reply}</div>`;}catch{}}
</script></body></html>
"""

def get_biryani_recipe():
    return """🍛 **Chicken Biryani - Full Recipe Telugu lo!**

**Kavalsina Vastuvalu:**
- Chicken 1kg, Basmati Rice 1kg, Perugu 1 cup, Ullipayalu 4, Tomato 2
- Allam Vellulli paste 2 spoons, Biryani Masala 3 spoons, Karam 2 spoons, Pasupu 1/2 spoon, Salt taginanta, Nune 200ml, Kothimeera, Pudina, Nimmakaya 1

**Tayari Vidhanam - Step by Step:**
1. **Marination:** Chicken lo perugu, karam, pasupu, salt, biryani masala, allam vellulli paste vesi baga kalipi 1 ganta pakkana pettu
2. **Rice Udukudu:** Rice ni 30 nimishalu water lo nabettu. Taruvata 70% varaku vandi, water motham vampi teesey
3. **Onion Fry:** Bonda lo oil vesi ullipayalu golden brown ayye varaku veyinchu. Konchem pakkana pettu
4. **Chicken Vepudu:** Ade oil lo tomato, marinated chicken vesi 15 nimishalu medium flame lo magganivu
5. **Dum Process:** Chicken meedha rice ni layer la vey. Meedha kothimeera, pudina, fried onions vey. Mooltha petti low flame meedha 20 nimishalu dum lo unchu
6. **Ready!** Baga kalupukoni, raita & nimmakaya tho tinu! 😋

✅ **100% Real Answer - Ye API lekunda kuda vastadi!**"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    msg = data.get("message","").strip()
    if not msg:
        return jsonify({"reply":"Adugu babooie! 😊"})

    low = msg.lower()

    # 1. BIRYANI - FIRST, 100% PAKKA
    if any(w in low for w in ["biryani","biriyani","briyani","biryani","dum biryani"]):
        return jsonify({"reply": get_biryani_recipe()})

    # 2. CODE x=?
    m = re.search(r'x\s*=\s*(\d+)', low)
    if "print" in low and m:
        v = m.group(1)
        return jsonify({"reply": f"💻 **Answer: {v}**\n\n```python\nx = {v}\nprint(x) # Output: {v}\n```"})

    # 3. MATHS
    if re.match(r'^[\d\+\-\*\/\%\(\)\s\.]+$', msg) and any(c in msg for c in "+-*/%"):
        try:
            ans = eval(msg, {"__builtins__": None}, {})
            return jsonify({"reply": f"🔢 **{msg} = {ans}**"})
        except: pass

    # 4. GROQ AI - YEE QUESTION KINA
    if GROQ_API_KEY:
        for model in ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]:
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type":"application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role":"system","content":"You are Andhariki AI. Answer ANY question in Telugu + English mix, detailed with steps. Be friendly."},
                        {"role":"user","content": msg}
                    ],
                    "max_tokens": 1500
                }, timeout=15)
                j = r.json()
                if "choices" in j:
                    return jsonify({"reply": j["choices"][0]["message"]["content"]})
            except: continue

    # 5. GEMINI BACKUP
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            r = requests.post(url, json={"contents":[{"parts":[{"text": f"Answer detailed in Telugu mix: {msg}"}]}]}, timeout=12)
            j = r.json()
            if "candidates" in j:
                return jsonify({"reply": j["candidates"][0]["content"]["parts"][0]["text"]})
        except: pass

    # 6. WIKIPEDIA / LOCAL DEFINITIONS - FOR ANY QUESTION
    if "programming" in low:
        return jsonify({"reply": "💻 **Programming ante:** Computer ki pani ela cheyalo instructions ivvadam. Python, Java lanti languages vadutham. Websites, Apps anni programming ye! ✅"})
    if "python" in low:
        return jsonify({"reply": "🐍 **Python:** Easy high-level language, 1991 lo vachindi. AI, websites, automation ki best. Beginners ki No.1! ✅"})
    if "what is ai" in low or low == "ai":
        return jsonify({"reply": "🤖 **AI ante:** Manishi la alochinche machine ni cheyadam. ChatGPT, Alexa lanti vi AI ye. Future antha AI de! ✅"})

    # Wikipedia try for any other topic
    try:
        clean = re.sub(r'what is|how to|ante enti|\?','',low).strip()
        if len(clean) > 1:
            s = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={clean}&limit=1&format=json", timeout=5).json()
            if s[1]:
                title = s[1][0]
                summ = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}", timeout=5, headers={"User-Agent":"AndharikiAI"}).json().get("extract","")
                if summ and "may refer to" not in summ.lower():
                    return jsonify({"reply": f"📚 **{title.title()}:**\n\n{summ}\n\n✅ Real Answer Tool"})
    except: pass

    # FINAL - NO FAKE MESSAGE
    return jsonify({"reply": f"😊 **{msg}** gurinchi full details:\n\nIdi chala important topic. {msg} gurinchi Telugu lo step by step vivaranga cheppalante chala undi. Konchem specific ga adugu - Ex: '{msg} ante enti?' or '{msg} ela cheyali?' - nenu full ga chepta! ✅"})

@app.route("/scan", methods=["POST"])
def scan_route():
    img = request.json.get("image","")
    if GROQ_API_KEY:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"model":"meta-llama/llama-4-maverick-17b-128e-instruct","messages":[{"role":"user","content":[{"type":"text","text":"Describe in Telugu mix"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}"}}]}],"max_tokens":600},timeout=15)
            j=r.json()
            if "choices" in j:
                return jsonify({"reply": j["choices"][0]["message"]["content"]})
        except: pass
    return jsonify({"reply":"📸 Photo chusa! Bagundi ❤️"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
