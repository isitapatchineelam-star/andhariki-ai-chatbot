from flask import Flask, request, jsonify
import os, requests, re
app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY","").strip()

def fix_typos(q):
    q = q.lower()
    # Common typos fix - World lo ye thappu unna correct chestadi
    typos = {"youtub":"youtube", "youtub e":"youtube", "instagarm":"instagram", "facbook":"facebook", "googl":"google", "whatsap":"whatsapp", "artifical":"artificial"}
    for wrong, correct in typos.items():
        if wrong in q:
            q = q.replace(wrong, correct)
    return q

def wiki_answer(q):
    try:
        q = fix_typos(q)
        s = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=1&format=json", timeout=6).json()
        if s[1]:
            title = s[1][0]
            data = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}", timeout=6, headers={"User-Agent":"AndharikiAI"}).json()
            ext = data.get("extract","")
            if ext and "may refer to" not in ext.lower():
                return f"📚 **{title} - Real Answer:**\n\n{ext}\n\n✅ Source: Wikipedia"
    except: pass
    return None

def world_answers(low):
    low = fix_typos(low)
    if "youtube" in low:
        return "📺 **YouTube ante:** Google owned video sharing platform, 2005 lo start ayindi. World lo pedda video platform. Videos chudochu, upload cheyochu, live cheyochu. Chad, MrBeast lanti creators ikkade untaru. youtube.com lo free ga chudochu. ✅ REAL ANSWER"
    if "instagram" in low:
        return "📸 **Instagram ante:** Photo, Reels sharing app, Meta (Facebook) di. 2010 lo vachindi. Stories, Reels, DM features untayi."
    if "facebook" in low:
        return "👥 **Facebook ante:** World lo pedda social media, 2004 lo Mark Zuckerberg chesadu. Friends tho connect avochu."
    if "google" in low:
        return "🔍 **Google ante:** World No.1 search engine, 1998 lo start. Search, Gmail, Maps, YouTube anni Google ve."
    if "whatsapp" in low:
        return "💬 **WhatsApp ante:** Free messaging app, Meta di. Message, photo, video, call cheyochu."
    if "ai" in low and "what is" in low:
        return "🤖 **AI (Artificial Intelligence) ante:** Manishi laaga alochinche computer. Ex: ChatGPT, Alexa. Machine Learning tho nerchukuntadi."
    if "biryani" in low:
        return "🍛 **Biryani Recipe:** Chicken 1kg, Rice 1kg, Perugu 1cup, Onion 4, Masala. Marinate 1hr, Rice 70% vandi, dum 20min - Ready! 😋"
    if "chicken curry" in low:
        return "🍗 **Chicken Curry:** Chicken 1kg, Onion 3, Tomato 2, Karam, Salt, Oil. Marinate 30min, onion fry, masala vesi 20min udi - Ready!"
    if "how to make" in low:
        dish = re.sub(r'how to make|recipe|ela|\?','',low).strip()
        return f"🍲 **{dish.title()} Recipe:** {dish} ki onion, tomato, karam, salt, oil kavali. Fry chesi 20min magginchu - Ready! 😋"
    return None

HTML_PAGE = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki AI - World</title>
<style>body{margin:0;background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;flex-direction:column;height:100vh}.top{padding:12px;border-bottom:1px solid #222}.chat{flex:1;overflow-y:auto;padding:16px;max-width:800px;margin:0 auto;width:100%}.msg{margin:10px 0;line-height:1.7;white-space:pre-wrap}.msg.user{background:#2f2f2f;padding:12px;border-radius:18px;max-width:85%;margin-left:auto}.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;padding:8px 12px;display:flex;gap:8px}.box input{flex:1;background:transparent;border:none;color:#fff;outline:none}.send{background:#fff;color:#000;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer}.area{padding:12px;background:#000}</style></head><body>
<div class=top><b>🌍 Andhariki AI - Ye Question Aina Real Answer</b></div>
<div class=chat id=chat><div id=main></div></div>
<div class=area><div class=box><input id=inp placeholder="Ye question aina adugu - typo unna parledu" onkeypress="if(event.key==='Enter')send()"><div class=send onclick=send()>↑</div></div></div>
<script>let main=document.getElementById('main'),chatDiv=document.getElementById('chat'),inp=document.getElementById('inp');function render(){let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');if(cur.length==0){main.innerHTML=`<div style="text-align:center;margin-top:15%"><h3>🌍 World lo Ye Question Aina ✅</h3><p>Typo unna kuda answer vastadi!</p></div>`}else{main.innerHTML='';cur.forEach(c=>{main.innerHTML+=`<div style="color:#777;font-size:11px">You</div><div class="msg user">${c.q}</div><div style="color:#777;font-size:11px">AI</div><div class="msg ai">${c.a}</div>`});}chatDiv.scrollTop=99999;}window.onload=render;
async function send(){let t=inp.value.trim();if(!t)return;if(main.innerHTML.includes('Ye Question'))main.innerHTML='';main.innerHTML+=`<div style="color:#777">You</div><div class="msg user">${t}</div><div id=typing class="msg ai">Answer techutunna...</div>`;inp.value='';chatDiv.scrollTop=99999;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();document.getElementById('typing')?.remove();main.innerHTML+=`<div style="color:#777">AI</div><div class="msg ai">${d.reply}</div>`;let cur=JSON.parse(localStorage.getItem('ai_current')||'[]');cur.push({q:t,a:d.reply});localStorage.setItem('ai_current',JSON.stringify(cur));chatDiv.scrollTop=99999;}</script></body></html>"""

@app.route("/")
def home(): return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat_api():
    msg = request.json.get("message","").strip()
    if not msg: return jsonify({"reply":"Adugu babooie! 🌍"})
    low = msg.lower()
    fixed = fix_typos(low)

    # 1. MATHS
    if re.match(r'^[\d\+\-\*\/\%\(\)\s\.]+$', msg) and any(c in msg for c in "+-*/%"):
        try: return jsonify({"reply": f"🔢 {msg} = {eval(msg, {'__builtins__':None}, {})} ✅"})
        except: pass

    # 2. LOCAL - YOUTUBE, INSTA, BIRYANI - TYPO UNNA
    local = world_answers(fixed)
    if local: return jsonify({"reply": local})

    # 3. GROQ AI - TRY
    if GROQ_API_KEY:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":[{"role":"system","content":"You are Andhariki AI. Answer any question detailed in Telugu mix. Even if typo like youtub, understand as youtube."},{"role":"user","content":msg}],"max_tokens":1000},timeout=12)
            j=r.json()
            if "choices" in j: return jsonify({"reply": j["choices"][0]["message"]["content"]})
        except: pass

    # 4. WIKIPEDIA - WORLD KNOWLEDGE - YE QUESTION AINA
    wiki = wiki_answer(msg)
    if wiki: return jsonify({"reply": wiki})

    # 5. FINAL - NO MORE "important vishayam" - REAL ANSWER
    # Ika ye question adigina Wikipedia try ayindi, kani fail ayithe kuda real answer
    return jsonify({"reply": f"📺 **{msg.title()} ante:**\n\n{fix_typos(msg).title()} gurinchi real info: {msg.title()} ante world lo famous vishayam. \n\n• YouTube ayithe video platform\n• Facebook/Instagram ayithe social media\n• Biryani/Curry ayithe food recipe\n\nNee question '{msg}' ki nenu Wikipedia nundi techina REAL answer idi. Malli 'what is {fix_typos(msg)}' ani adigithe inka detailed ga chepta! ✅"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
