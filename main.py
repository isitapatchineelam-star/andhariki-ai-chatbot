from flask import Flask, request, jsonify
import os, requests, urllib.parse
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

# REAL INDIAN CULTURE - REAL TEMPLE PHOTOS - 100% TRADITIONAL - FULLY CLOSED
# These are real Wikimedia temple photos - NOT AI generated - so chest open never comes
REAL_TEMPLE_PHOTOS = {
"rama": [
"https://upload.wikimedia.org/wikipedia/commons/8/8a/Rama_with_his_bow.jpg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Rama_with_his_bow.jpg/500px-Rama_with_his_bow.jpg",
"https://upload.wikimedia.org/wikipedia/commons/1/1b/Rama_Sita.jpg"
],
"krishna": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Krishna_and_Radha_in_a_Pavilion.jpg/500px-Krishna_and_Radha_in_a_Pavilion.jpg",
"https://upload.wikimedia.org/wikipedia/commons/7/7e/Krishna_flute.jpg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Krishna_Govardhan.jpg/500px-Krishna_Govardhan.jpg"
],
"shiva": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Shiva_as_the_Lord_of_Music.jpg/500px-Shiva_as_the_Lord_of_Music.jpg",
"https://upload.wikimedia.org/wikipedia/commons/0/0d/Shiva_statue.jpg"
],
"ganesh": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ganesha_Basohli_miniature_circa_1730.jpg/500px-Ganesha_Basohli_miniature_circa_1730.jpg",
"https://upload.wikimedia.org/wikipedia/commons/4/4f/Ganesha.jpg"
],
"hanuman": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hanuman_carries_Rama.jpg/500px-Hanuman_carries_Rama.jpg",
"https://upload.wikimedia.org/wikipedia/commons/6/6f/Hanuman_in_Sunderkand.jpg"
],
"durga": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Durga_Mahishasura_Mardini.jpg/500px-Durga_Mahishasura_Mardini.jpg",
"https://upload.wikimedia.org/wikipedia/commons/0/0e/Durga_Puja_Idol.jpg"
],
"lakshmi": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Lakshmi.jpg/500px-Lakshmi.jpg"
],
"venkateswara": [
"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Tirupati_Balaji.jpg/500px-Tirupati_Balaji.jpg"
]
}

def get_real_temple_image(query):
    low=query.lower()
    for god, urls in REAL_TEMPLE_PHOTOS.items():
        if god in low:
            import random
            return random.choice(urls)
    return None

def ask_ai(history, lang="auto"):
    lang_i = f"Reply ONLY in {lang}. " if lang!="auto" else "Auto detect same language. "
    sys = f"You are Andhariki-AI Personal Assistant by Andhariki Team. {lang_i} You work exactly like best AI with all features - chat, coding, writing, translation, education, search, email, stories, explain, debug everything. Be helpful respectful. Call user babooie. Never say ChatGPT, OpenAI, GPT. You are Andhariki-AI only."
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
<div class="side"><div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍 Real Indian Culture</span></div>
<div class="lang-box"><div style="font-size:11px;opacity:.6">🌍 Bhasha</div><select id="langSel" onchange="saveLang()"><option value="auto">Auto Detect</option><option value="te">Telugu తెలుగు</option><option value="en">English</option><option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option><option value="ml">Malayalam</option></select></div>
<div class="item" onclick="quick('create image lord rama real temple')">🖼️ Gods - Real Indian Temple Photos - Fully Dressed</div><div class="item" onclick="quickSearch()">🌐 Search the Web</div><div class="item" onclick="quick('Write a love story in Telugu')">✏️ Writing / Email</div><div class="item" onclick="quick('Translate to English: Nenu bagunna')">🌍 Translate</div><div class="item" onclick="quick('Python code for calculator with explanation')">💻 Code - Like Best AI</div><div class="item" onclick="quick('Explain black hole in simple Telugu')">📚 Education</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div><div id="rlist" style="margin-top:8px"></div></div>
<div class="main"><div class="top"><div>✨ Andhariki-AI - Real Traditional Indian Culture</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:5px 12px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center"><h3>Namaste babooie! Nenu Andhariki-AI 🙏</h3><p style="font-size:12px;opacity:.6">Real Temple Photos - Raja Ravi Varma Paintings - 100% Traditional Indian Culture - Full Dress - No Open Chest!</p>
<div class="opt" onclick="quick('create image lord rama real temple')">🙏 Rama - Real Temple Photo</div><div class="opt" onclick="quick('create image lord krishna real temple')">🦚 Krishna - Real Temple Photo</div><div class="opt" onclick="quick('create image lord ganesh real temple')">🐘 Ganesh - Real Temple Photo</div><div class="opt" onclick="quick('create image goddess durga real temple')">🌺 Durga - Real Temple Photo</div><div class="opt" onclick="quick('Write python code for student marks')">💻 Code Like Best AI</div></div></div></div>
<div style="padding:14px"><div class="box"><button class="icon" onclick="quick('create image ')">+</button><input id="inp" placeholder="Emaina adugu babooie..." onkeypress="if(event.key==='Enter')send()"><button class="icon" onclick="startVoice()">🎤</button><button class="send" onclick="send()">↑</button></div><div style="text-align:center;font-size:10px;opacity:.25;margin-top:6px">Andhariki-AI - Real Indian Culture Traditional - 100% Full Dress - Made with ❤️</div></div></div><button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'auto';document.getElementById('langSel').value=curLang;let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel()}function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🌍 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){let l=document.getElementById('rlist');l.innerHTML='';recents.slice(0,15).forEach((t,i)=>{let d=document.createElement('div');d.className='rec-item';d.innerHTML=`<span class=rec-text onclick="quick('${t.replace(/'/g," ")}')">${t.substring(0,35)}</span><span onclick='deleteOne(${i})' style=cursor:pointer>❌</span>`;l.appendChild(d)})}renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Delete cheyala babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>New Chat Started ✅</h3><p>Andhariki-AI Ready - Real Traditional Indian Culture!</p></div>';history=[]}}function newChat(){clearAll()}function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}
async function send(){let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;let low=text.toLowerCase();
if(low.includes('image')||low.includes('photo')||low.includes('rama')||low.includes('krishna')||low.includes('shiva')||low.includes('ganesh')||low.includes('hanuman')||low.includes('durga')||low.includes('lakshmi')||low.includes('venkateswara')||low.includes('ayyappa')||low.includes('sai')||low.includes('bommaru')){addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();inp.value='';let r=await fetch('/get_real_image?q='+encodeURIComponent(text));let d=await r.json();let url=d.url;if(!url){addMsg('Babooie, aa god ki real photo dorakaledu - malli try chey','assistant');return;}let imgHTML=`<div style="margin-top:10px">Idigo babooie - Real Indian Temple Photo - 100% Traditional Full Dress 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download HD - Real Temple Photo</a></div>`;addMsg(imgHTML,'assistant');return;}
addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();history.push({role:'user',content:text});inp.value='';let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Andhariki-AI alochistondi...';document.getElementById('msgs').appendChild(ty);try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});}catch(e){ty.textContent='GROQ_API_KEY check chey babooie!'}}function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}async function quickSearch(){let q=prompt('Em search cheyali?');if(!q)return;addMsg('Nuvvu: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}</script></body></html>"""

@app.route("/chat", methods=["POST"])
def chat_api():
    d=request.json
    return jsonify({"reply": ask_ai(d.get("history",[]), d.get("lang","auto"))})

@app.route("/get_real_image")
def get_real_image():
    q=request.args.get("q","")
    url=get_real_temple_image(q)
    if not url:
        # fallback - return rama as default traditional
        url="https://upload.wikimedia.org/wikipedia/commons/8/8a/Rama_with_his_bow.jpg"
    return jsonify({"url": url})

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
