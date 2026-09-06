from flask import Flask, request, jsonify
import os, requests, urllib.parse
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

# REAL INDIAN TEMPLE IDOL - 100% TRADITIONAL REAL PHOTO STYLE
REAL_GODS = {
"rama": "Real photograph of Lord Rama idol in Ayodhya Ram Mandir, ancient Indian temple stone sculpture, wearing real golden silk dhoti kurta fully closed chest covered, golden kireeta mukutam, pearl necklace, tilak, holding bow arrow, garland flowers, temple oil lamp background, ultra realistic 8k photograph, traditional Indian culture, divine respectful NOT modern NOT cartoon NOT topless",
"krishna": "Real photograph of Lord Krishna idol in Vrindavan ISKCON temple, blue stone idol, wearing real golden silk kurta fully closed buttoned chest 100 percent covered no skin, yellow silk dhoti orange angavastram, peacock feather mukut, pearl haram, flute, flower garland, temple background, ultra realistic 8k traditional Indian culture photograph, NOT modern NOT cartoon NOT topless divine",
"shiva": "Real photograph of Lord Shiva lingam and idol in Kashi Vishwanath temple, wearing rudraksha mala tripundra tiger skin silk dhoti chest covered with vibhuti, trishul damru, realistic temple photograph traditional Indian culture NOT topless divine",
"ganesh": "Real photograph of Lord Ganesha idol in Siddhivinayak Mumbai temple, elephant head, wearing real red golden silk dhoti kurta chest covered, golden crown, modak, flower garland, realistic temple photograph traditional Indian culture divine",
"hanuman": "Real photograph of Lord Hanuman idol in Ayodhya, wearing real orange silk dhoti kurta fully closed chest covered, golden crown, gada mace, sindoor, realistic temple photograph traditional Indian culture NOT topless",
"durga": "Real photograph of Goddess Durga idol in Kolkata Durga Puja pandal, wearing real red Banarasi silk saree with fully closed blouse chest fully covered, golden crown, 10 hands weapons lion, garland, ultra realistic temple photograph traditional Indian culture modest respectful",
"lakshmi": "Real photograph of Goddess Lakshmi idol in temple, wearing real red silk saree fully closed blouse chest covered, golden crown lotus coins, realistic temple photograph traditional Indian culture",
"saraswati": "Real photograph of Goddess Saraswati idol, wearing real white silk saree fully closed blouse chest covered, veena book, realistic temple photograph traditional",
"venkateswara": "Real photograph of Lord Venkateswara Tirupati Balaji idol, wearing real golden silk dhoti chest covered, diamond crown tilak, flower garland, Tirumala temple background, ultra realistic photograph traditional Indian culture",
"ayyappa": "Real photograph of Lord Ayyappa Sabarimala idol, wearing black dhoti golden ornaments crown chest covered, realistic Kerala temple photograph traditional",
"saibaba": "Real photograph of Shirdi Sai Baba idol in Shirdi temple, wearing white kafni fully closed chest covered, realistic temple photograph traditional"
}

def get_real_prompt(q):
    low=q.lower()
    for k,v in REAL_GODS.items():
        if k in low: return v
    clean=q.replace("create image","").replace("image","").replace("bommaru","").strip()[:70]
    return f"Real photograph of {clean} idol in ancient Indian temple, real silk traditional dress kurta dhoti saree fully closed chest 100 percent covered thick fabric no skin visible no topless no bare chest, golden crown tilak flower garland, ultra realistic 8k photograph, traditional Indian culture, temple oil lamp background, divine respectful NOT modern NOT cartoon NOT anime"

def ask_ai(history, lang="auto"):
    lang_i = f"Reply ONLY in {lang}. " if lang!="auto" else "Auto detect same language. "
    sys = f"You are Andhariki-AI Personal Assistant by Andhariki Team. {lang_i} You work exactly like best AI - you do chat, coding, writing, translation, education, search summary, email, stories, explain, debug everything perfectly. Be helpful respectful. Call user babooie lovingly. Never ever say ChatGPT, OpenAI, GPT. You are Andhariki-AI only."
    msgs=[{"role":"system","content":sys}]
    for h in history[-15:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},json={"model":"openai/gpt-oss-20b","messages":msgs,"temperature":0.7,"max_tokens":3000},timeout=35)
        d=r.json()
        if "choices" in d: return d['choices'][0]['message']['content']
        return str(d)[:400]
    except Exception as e: return f"Error: {e}"

@app.route("/")
def home():
    return """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki-AI Personal Assistant</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#000;color:#fff;display:flex;height:100vh}.side{width:280px;background:#171717;padding:14px;overflow:auto;display:flex;flex-direction:column}.logo{font-weight:900;font-size:20px}.logo span{font-size:11px;opacity:.5;font-weight:400}.lang-box{margin:12px 0;background:#2f2f2f;padding:10px;border-radius:12px}.lang-box select{width:100%;background:#212121;color:#fff;border:1px solid #444;padding:8px;border-radius:8px;margin-top:6px}.item{padding:10px;border-radius:10px;opacity:.75;font-size:13px;cursor:pointer;display:flex;gap:10px;margin-top:4px;background:#212121}.item:hover{background:#2f2f2f;opacity:1}.rtitle{font-size:11px;opacity:.5;margin-top:16px;display:flex;justify-content:space-between}.clear-btn{background:#ff3333;color:#fff;border:none;padding:4px 8px;border-radius:6px;font-size:10px;cursor:pointer}.rec-item{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;background:#2f2f2f;margin-bottom:5px;border-radius:8px}.rec-text{font-size:12px;opacity:.7;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}.main{flex:1;background:#212121;display:flex;flex-direction:column}.top{padding:12px 16px;border-bottom:1px solid #333;display:flex;justify-content:space-between;font-weight:700}.chat{flex:1;overflow:auto;padding:20px;max-width:850px;margin:0 auto;width:100%}.msg{margin:14px 0;line-height:1.7;white-space:pre-wrap;word-wrap:break-word}.assistant{background:#2f2f2f;padding:14px 16px;border-radius:16px}.center{max-width:560px;margin:30px auto;display:flex;flex-direction:column;gap:8px;text-align:center}.opt{opacity:.8;cursor:pointer;padding:12px;border-radius:12px;background:#2f2f2f;display:flex;gap:10px;text-align:left}.opt:hover{opacity:1}.box{max-width:850px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:12px 16px;gap:8px}.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:15px}.icon{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:.7}.send{background:#fff;color:#000;width:34px;height:34px;border-radius:50%;border:none;cursor:pointer;font-weight:800}.newchat{position:fixed;bottom:16px;left:16px;background:#3b82f6;color:#fff;border:none;padding:10px 18px;border-radius:24px;font-weight:600;cursor:pointer}@media(max-width:768px){.side{display:none}}</style></head><body>
<div class="side"><div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍 Real Traditional</span></div>
<div class="lang-box"><div style="font-size:11px;opacity:.6">🌍 Bhasha</div><select id="langSel" onchange="saveLang()"><option value="auto">Auto Detect</option><option value="te">Telugu తెలుగు</option><option value="en">English</option><option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option><option value="ml">Malayalam</option></select></div>
<div class="item" onclick="quick('create image lord rama real temple idol photograph traditional')">🖼️ God Images - Real Temple Photo - Traditional</div><div class="item" onclick="quickSearch()">🌐 Search the Web - Working</div><div class="item" onclick="quick('Write a love story in Telugu')">✏️ Writing / Email / Essay</div><div class="item" onclick="quick('Translate to English: Nenu bagunna')">🌍 Translate Any Language</div><div class="item" onclick="quick('Python code for calculator with explanation')">💻 Code - Like Best AI</div><div class="item" onclick="quick('Explain black hole in simple Telugu')">📚 Education - Explain</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div><div id="rlist" style="margin-top:8px"></div></div>
<div class="main"><div class="top"><div>✨ Andhariki-AI - Real Traditional Culture</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:5px 12px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center"><h3>Namaste babooie! Nenu Andhariki-AI 🙏</h3><p style="font-size:12px;opacity:.6">Real Indian Temple Idols - Real Culture Traditional Photo Style - NOT Cartoon!</p>
<div class="opt" onclick="quick('create image lord rama real temple idol photograph traditional indian culture')">🙏 Rama - Real Temple Photo</div><div class="opt" onclick="quick('create image lord krishna real temple idol photograph')">🦚 Krishna - Real Temple Photo</div><div class="opt" onclick="quick('create image lord shiva real temple idol')">🔱 Shiva - Real Temple Photo</div><div class="opt" onclick="quick('create image goddess durga real temple idol red saree')">🌺 Durga - Real Saree Photo</div><div class="opt" onclick="quick('Write python code for student marks')">💻 Code Like Best AI</div></div></div></div>
<div style="padding:14px"><div class="box"><button class="icon" onclick="quick('create image ')">+</button><input id="inp" placeholder="Emaina adugu babooie..." onkeypress="if(event.key==='Enter')send()"><button class="icon" onclick="startVoice()">🎤</button><button class="send" onclick="send()">↑</button></div><div style="text-align:center;font-size:10px;opacity:.25;margin-top:6px">Andhariki-AI - Real Traditional Indian Culture - Made with ❤️</div></div></div><button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'auto';document.getElementById('langSel').value=curLang;let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel()}function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🌍 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){let l=document.getElementById('rlist');l.innerHTML='';recents.slice(0,15).forEach((t,i)=>{let d=document.createElement('div');d.className='rec-item';d.innerHTML=`<span class=rec-text onclick="quick('${t.replace(/'/g," ")}')">${t.substring(0,35)}</span><span onclick='deleteOne(${i})' style=cursor:pointer>❌</span>`;l.appendChild(d)})}renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Delete cheyala babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>New Chat Started ✅</h3><p>Andhariki-AI Ready - Real Traditional!</p></div>';history=[]}}function newChat(){clearAll()}function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}
async function send(){let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;let low=text.toLowerCase();
if(low.includes('image')||low.includes('photo')||low.includes('rama')||low.includes('krishna')||low.includes('shiva')||low.includes('ganesh')||low.includes('hanuman')||low.includes('durga')||low.includes('lakshmi')||low.includes('venkateswara')||low.includes('ayyappa')||low.includes('sai')||low.includes('bommaru')){addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();inp.value='';let r=await fetch('/make_image_prompt?q='+encodeURIComponent(text));let d=await r.json();let prompt=d.prompt;addMsg('🎨 Real traditional temple photo chestondi babooie...','assistant');let seed=Math.floor(Math.random()*999999);let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=768&model=flux&nologo=true&seed=${seed}&enhance=true`;let imgHTML=`<div style="margin-top:10px">Idigo babooie - Real Temple Idol - Traditional Indian Culture 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download HD</a></div>`;setTimeout(()=>addMsg(imgHTML,'assistant'),900);return;}
addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();history.push({role:'user',content:text});inp.value='';let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Andhariki-AI alochistondi...';document.getElementById('msgs').appendChild(ty);try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});}catch(e){ty.textContent='GROQ_API_KEY check chey babooie!'}}function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}async function quickSearch(){let q=prompt('Em search cheyali?');if(!q)return;addMsg('Nuvvu: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}</script></body></html>"""

@app.route("/chat", methods=["POST"])
def chat_api():
    d=request.json
    return jsonify({"reply": ask_ai(d.get("history",[]), d.get("lang","auto"))})

@app.route("/make_image_prompt")
def make_image_prompt():
    q=request.args.get("q","")
    return jsonify({"prompt": get_real_prompt(q)})

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
