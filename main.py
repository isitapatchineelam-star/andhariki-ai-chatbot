from flask import Flask, request, jsonify
import os, requests, urllib.parse, random
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

REAL_GODS = {
"rama": "Real stone statue of Lord Rama in Ayodhya Ram Mandir, golden embroidered achkan kurta buttoned up to neck high collar long sleeves thick fabric chest 100 percent covered no skin visible, orange dhoti golden border, golden kireeta mukut crown, pearl mala, bow arrow, marigold garland, oil diyas temple background, ultra realistic 8k traditional Indian culture divine respectful fully clothed",
"krishna": "Real stone statue of Lord Krishna in Vrindavan temple blue skin, golden embroidered achkan kurta buttoned up to neck long sleeves chest 100 percent covered no skin visible, yellow silk dhoti, peacock feather golden mukut, pearl haram, flute, flower garland, temple background ultra realistic 8k traditional fully clothed",
"shiva": "Real stone statue of Lord Shiva in Kashi temple, wearing fully closed saffron kurta chest 100 percent covered rudraksha mala, trishul damru, realistic temple photograph traditional fully clothed",
"ganesh": "Real stone statue of Lord Ganesha in Siddhivinayak temple elephant head, wearing fully closed red golden kurta dhoti chest fully covered, golden crown modak garland, realistic temple photo traditional fully clothed",
"hanuman": "Real stone statue of Lord Hanuman in temple, wearing fully closed orange kurta dhoti buttoned chest fully covered, golden crown gada mace sindoor, realistic temple photo traditional",
"durga": "Real clay idol of Goddess Durga in Kolkata Durga Puja pandal, wearing fully closed red Banarasi silk saree with fully closed long sleeve blouse thick fabric chest 100 percent covered belly fully covered no midriff no cleavage no belly visible, golden crown mukut 10 hands weapons trishul chakra lion vahana marigold garland, ultra realistic 8k traditional Indian culture fully clothed modest respectful divine mother",
"lakshmi": "Real idol of Goddess Lakshmi in temple, wearing fully closed red silk saree fully closed blouse chest 100 percent covered no cleavage, golden crown lotus, realistic traditional fully clothed",
"saraswati": "Real idol of Goddess Saraswati, wearing fully closed white silk saree fully closed blouse chest fully covered, veena book, realistic traditional fully clothed",
"venkateswara": "Real idol of Lord Venkateswara Tirupati Balaji, wearing fully closed golden silk dhoti kurta buttoned chest 100 percent covered, diamond crown tilak garland, realistic temple photo fully clothed",
"ayyappa": "Real idol of Lord Ayyappa Sabarimala, wearing fully closed black kurta dhoti buttoned chest fully covered, golden ornaments crown, realistic temple photo fully clothed",
"saibaba": "Real idol of Shirdi Sai Baba, wearing fully closed white kafni kurta buttoned chest fully covered, realistic temple photo fully clothed"
}

def get_prompt(q):
    low=q.lower()
    for k,v in REAL_GODS.items():
        if k in low:
            return v
    clean=q.replace("create image","").replace("image","").replace("bommaru","").strip()[:60]
    return f"Real stone statue of {clean} in ancient Indian temple, wearing fully closed thick fabric kurta buttoned up to neck chest 100 percent covered belly covered no skin visible no bare chest no topless no midriff, real silk dhoti saree golden crown tilak flower garland, ultra realistic 8k photograph traditional Indian culture temple oil lamp background divine respectful fully clothed NOT cartoon NOT anime"

def ask_ai(history, lang="auto"):
    if lang=="te": li="Reply ONLY in Telugu. "
    elif lang=="en": li="Reply ONLY in English. "
    elif lang=="hi": li="Reply ONLY in Hindi. "
    elif lang=="ta": li="Reply ONLY in Tamil. "
    elif lang=="kn": li="Reply ONLY in Kannada. "
    elif lang=="ml": li="Reply ONLY in Malayalam. "
    else: li="Auto detect user language and reply in SAME language the user used. "
    sys=f"You are Andhariki-AI Personal Assistant created by Andhariki Team. {li} You can do everything - chat, coding, writing, translation, education, search, email, stories, explain, debug, all features. You are helpful respectful. Call user babooie. You are Andhariki-AI only, built by Andhariki Team. Language must stay {lang}."
    msgs=[{"role":"system","content":sys}]
    for h in history[-15:]:
        if h.get('role') in ['user','assistant']:
            msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},json={"model":"openai/gpt-oss-20b","messages":msgs,"temperature":0.6,"max_tokens":3000},timeout=35)
        d=r.json()
        if "choices" in d:
            return d['choices'][0]['message']['content']
        return str(d)[:400]
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def home():
    return """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki-AI Personal Assistant</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#000;color:#fff;display:flex;height:100vh}.side{width:280px;background:#171717;padding:14px;overflow:auto;display:flex;flex-direction:column}.logo{font-weight:900;font-size:20px}.logo span{font-size:11px;opacity:.5;font-weight:400}.lang-box{margin:12px 0;background:#2f2f2f;padding:12px;border-radius:12px;border:2px solid #3b82f6}.lang-box select{width:100%;background:#212121;color:#fff;border:1px solid #555;padding:10px;border-radius:8px;margin-top:6px;font-weight:600}.item{padding:10px;border-radius:10px;opacity:.9;font-size:13px;cursor:pointer;display:flex;gap:10px;margin-top:4px;background:#212121}.item:hover{background:#2f2f2f}.rtitle{font-size:11px;opacity:.5;margin-top:16px;display:flex;justify-content:space-between}.clear-btn{background:#ff3333;color:#fff;border:none;padding:4px 8px;border-radius:6px;font-size:10px;cursor:pointer}.rec-item{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;background:#2f2f2f;margin-bottom:5px;border-radius:8px}.rec-text{font-size:12px;opacity:.7;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}.main{flex:1;background:#212121;display:flex;flex-direction:column}.top{padding:12px 16px;border-bottom:1px solid #333;display:flex;justify-content:space-between;font-weight:700}.chat{flex:1;overflow:auto;padding:20px;max-width:850px;margin:0 auto;width:100%}.msg{margin:14px 0;line-height:1.7;white-space:pre-wrap;word-wrap:break-word}.assistant{background:#2f2f2f;padding:14px 16px;border-radius:16px}.center{max-width:560px;margin:30px auto;display:flex;flex-direction:column;gap:8px;text-align:center}.opt{opacity:.9;cursor:pointer;padding:12px;border-radius:12px;background:#2f2f2f;display:flex;gap:10px;text-align:left}.opt:hover{background:#3a3a3a}.box{max-width:850px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:12px 16px;gap:8px}.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:15px}.icon{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:.7}.send{background:#fff;color:#000;width:34px;height:34px;border-radius:50%;border:none;cursor:pointer;font-weight:800}.newchat{position:fixed;bottom:16px;left:16px;background:#3b82f6;color:#fff;border:none;padding:10px 18px;border-radius:24px;font-weight:600;cursor:pointer}@media(max-width:768px){.side{display:none}}</style></head><body>
<div class="side"><div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍 All Features</span></div>
<div class="lang-box"><div style="font-size:12px;font-weight:700">🌍 Bhasha - LOCK Chey</div><select id="langSel" onchange="saveLang()"><option value="te">Telugu తెలుగు - LOCK</option><option value="auto">Auto Detect</option><option value="en">English - LOCK</option><option value="hi">Hindi - LOCK</option><option value="ta">Tamil - LOCK</option><option value="kn">Kannada - LOCK</option><option value="ml">Malayalam - LOCK</option></select><div style="font-size:10px;opacity:.6;margin-top:6px">Select cheste maradu!</div></div>
<div class="item" onclick="quick('create image lord rama real temple fully closed dress')">🙏 Rama - Real Temple</div><div class="item" onclick="quick('create image lord krishna real temple fully closed dress')">🦚 Krishna - Real</div><div class="item" onclick="quick('create image lord shiva real temple fully closed')">🔱 Shiva - Real</div><div class="item" onclick="quick('create image lord ganesh real temple')">🐘 Ganesh - Real</div><div class="item" onclick="quick('create image lord hanuman real temple')">🐒 Hanuman - Real</div><div class="item" onclick="quick('create image goddess durga real temple fully closed saree belly covered')">🌺 Durga - Real - Fully Closed</div><div class="item" onclick="quick('create image goddess lakshmi real temple')">💰 Lakshmi - Real</div><div class="item" onclick="quick('create image lord venkateswara real temple')">🕉️ Balaji - Real</div><div class="item" onclick="quick('create image lord ayyappa real temple')">🙏 Ayyappa - Real</div><div class="item" onclick="quick('create image saibaba real temple')">🌟 Sai Baba - Real</div><div class="item" onclick="quickSearch()">🌐 Search the Web</div><div class="item" onclick="quick('Python lo calculator code rayi')">💻 Code - Andhariki-AI</div><div class="item" onclick="quick('Translate to English: Nenu bagunna')">🌍 Translate</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div><div id="rlist" style="margin-top:8px"></div></div>
<div class="main"><div class="top"><div>✨ Andhariki-AI - All Features Working</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:5px 12px;border-radius:12px;border:1px solid #3b82f6">🔒 Telugu</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center"><h3>Namaste babooie! Nenu Andhariki-AI 🙏</h3><p style="font-size:12px;opacity:.7">Andhariki-AI lo anni features - Chat, Real God Images Fully Closed Dress, Search, Translate, Code, Writing, Education, Voice - anni working! Language LOCK!</p>
<div class="opt" onclick="quick('create image lord rama real temple fully closed dress')">🙏 Rama - Real Temple - Fully Closed - Working</div><div class="opt" onclick="quick('create image goddess durga real temple fully closed saree belly covered')">🌺 Durga - Real - Fully Closed Saree - Belly Covered - Fixed</div><div class="opt" onclick="quick('create image lord krishna real temple fully closed dress')">🦚 Krishna - Real Temple - Working</div><div class="opt" onclick="quick('Python lo calculator code rayi with explanation')">💻 Code - Andhariki-AI</div><div class="opt" onclick="quick('Nenu ela unnanu?')">💬 Language Test</div></div></div></div>
<div style="padding:14px"><div class="box"><button class="icon" onclick="quick('create image ')">+</button><input id="inp" placeholder="Emaina adugu babooie... Andhariki-AI ready!" onkeypress="if(event.key==='Enter')send()"><button class="icon" onclick="startVoice()">🎤</button><button class="send" onclick="send()">↑</button></div><div style="text-align:center;font-size:10px;opacity:.25;margin-top:6px">Andhariki-AI Personal Assistant - All Features - Language Lock + Real Gods Fully Closed - Made with ❤️ by Andhariki Team</div></div></div><button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'te';document.getElementById('langSel').value=curLang;let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel();alert('Language '+curLang+' LOCK ayindi babooie! Ippudu maradu!')}function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🔒 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){let l=document.getElementById('rlist');l.innerHTML='';recents.slice(0,15).forEach((t,i)=>{let d=document.createElement('div');d.className='rec-item';d.innerHTML=`<span class=rec-text onclick="quick('${t.replace(/'/g," ")}')">${t.substring(0,35)}</span><span onclick='deleteOne(${i})' style=cursor:pointer>❌</span>`;l.appendChild(d)})}renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Delete cheyala babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>New Chat Started ✅</h3><p>Language '+curLang+' LOCK - All Gods Ready!</p></div>';history=[]}}function newChat(){clearAll()}function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}
async function send(){let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;let low=text.toLowerCase();
if(low.includes('image')||low.includes('photo')||low.includes('rama')||low.includes('krishna')||low.includes('shiva')||low.includes('ganesh')||low.includes('hanuman')||low.includes('durga')||low.includes('lakshmi')||low.includes('saraswati')||low.includes('venkateswara')||low.includes('balaji')||low.includes('ayyappa')||low.includes('sai')||low.includes('bommaru')){addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();inp.value='';let r=await fetch('/make_image_prompt?q='+encodeURIComponent(text));let d=await r.json();let prompt=d.prompt;addMsg('🎨 Andhariki-AI real traditional temple idol chestondi babooie...','assistant');let seed=Math.floor(Math.random()*999999);let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=768&height=1024&model=flux&nologo=true&seed=${seed}&enhance=true`;let imgHTML=`<div style="margin-top:10px">Idigo babooie - Real Temple Idol - Fully Closed - Andhariki-AI 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download HD</a><br><span style="font-size:10px;opacity:.5">Andhariki-AI Real Temple - Fully Closed - Traditional</span></div>`;setTimeout(()=>addMsg(imgHTML,'assistant'),900);return;}
addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();history.push({role:'user',content:text});inp.value='';let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Andhariki-AI alochistondi...';document.getElementById('msgs').appendChild(ty);try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});}catch(e){ty.textContent='GROQ_API_KEY check chey babooie!'}}function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN','en':'en-US'};let l=m[curLang]||'te-IN';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}async function quickSearch(){let q=prompt('Em search cheyali babooie?');if(!q)return;addMsg('Nuvvu: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}</script></body></html>"""

@app.route("/chat", methods=["POST"])
def chat_api():
    d=request.json
    return jsonify({"reply": ask_ai(d.get("history",[]), d.get("lang","auto"))})

@app.route("/make_image_prompt")
def make_image_prompt():
    q=request.args.get("q","")
    return jsonify({"prompt": get_prompt(q)})

@app.route("/search")
def search_route():
    q=request.args.get("q",""); lang=request.args.get("lang","auto")
    try:
        info=requests.get(f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json",timeout=8).json().get("AbstractText","")[:500]
        return jsonify({"result": ask_ai([{"role":"user","content":f"Search: {q}. Info: {info}"}], lang)})
    except:
        return jsonify({"result": ask_ai([{"role":"user","content":q}], lang)})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
