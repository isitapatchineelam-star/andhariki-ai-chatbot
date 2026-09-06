from flask import Flask, request, jsonify
import os, requests, urllib.parse

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

# ALL GODS 100% TRADITIONAL FULL DRESS PROMPTS
GOD_PROMPTS = {
"rama": "Adult male Lord Rama age 26 Ayodhya king wearing FULLY COVERED golden embroidered achkan kurta high collar long sleeves chest fully covered orange dhoti angavastram golden mukut crown holding bow arrow NOT topless NOT bare chest divine royal",
"krishna": "Adult male Lord Krishna age 25 blue skin Dwarka prince wearing FULLY COVERED golden embroidered achkan kurta high collar long sleeves chest fully covered yellow dhoti orange angavastram peacock feather crown playing flute NOT topless NOT bare chest divine",
"shiva": "Adult male Lord Shiva age 32 meditating wearing FULLY COVERED tiger skin rudraksha mala tripundra trishul damru orange dhoti chest covered with ash and rudraksha NOT topless divine",
"ganesh": "Lord Ganesha elephant head cute god wearing FULLY COVERED golden kurta orange dhoti crown modak holding NOT topless divine traditional",
"hanuman": "Lord Hanuman muscular vanara wearing FULLY COVERED orange kurta dhoti gada mace chest covered with sindoor NOT topless divine",
"durga": "Goddess Durga Maa wearing FULLY COVERED red saree golden blouse crown trishul lion NOT revealing traditional temple style",
"lakshmi": "Goddess Lakshmi Maa wearing FULLY COVERED red saree golden blouse lotus crown coins NOT revealing divine",
"saraswati": "Goddess Saraswati Maa wearing FULLY COVERED white saree veena book divine",
"venkateswara": "Lord Venkateswara Tirupati Balaji wearing FULLY COVERED golden silk dhoti crown tilak chest covered divine",
"ayyappa": "Lord Ayyappa wearing FULLY COVERED black dhoti golden ornaments crown chest covered divine",
"saibaba": "Sai Baba Shirdi wearing FULLY COVERED white kafni cloth chest covered divine"
}

def get_god_prompt(text):
    low=text.lower()
    for god_key in GOD_PROMPTS:
        if god_key in low:
            return GOD_PROMPTS[god_key]
    # generic god - always fully covered
    clean=text.replace("create image","").replace("image","").replace("photo","").strip()[:60]
    return f"{clean} wearing FULLY COVERED traditional Indian temple royal dress kurta dhoti saree chest fully covered NOT topless NOT bare chest NOT revealing modest divine 4k"

def ask_ai(history, lang="auto"):
    lang_instr = f"Reply ONLY in {lang} language. " if lang!="auto" else "Auto detect user language and reply same language. "
    msgs=[{"role":"system","content":f"You are Andhariki-AI Personal Assistant built by Andhariki Team. {lang_instr} You can do everything - coding, writing, education, translation, search, stories. Always respectful. Call user babooie lovingly. Never say you are ChatGPT or OpenAI. You are Andhariki-AI only."}]
    for h in history[-15:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"openai/gpt-oss-20b","messages":msgs,"temperature":0.7,"max_tokens":2500},timeout=35)
        d=r.json()
        if "choices" in d: return d['choices'][0]['message']['content']
        return "Andhariki-AI busy babooie: "+str(d)[:300]
    except Exception as e: return f"Error babooie: {e}"

@app.route("/")
def home():
    return """
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>Andhariki-AI Personal Assistant</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#000;color:#fff;display:flex;height:100vh}
.side{width:280px;background:#171717;padding:14px;overflow:auto;display:flex;flex-direction:column}
.logo{font-weight:900;font-size:20px}.logo span{font-size:11px;opacity:.5;font-weight:400}
.lang-box{margin:12px 0;background:#2f2f2f;padding:10px;border-radius:12px}
.lang-box select{width:100%;background:#212121;color:#fff;border:1px solid #444;padding:8px;border-radius:8px;margin-top:6px}
.item{padding:10px;border-radius:10px;opacity:.75;font-size:13px;cursor:pointer;display:flex;gap:10px;margin-top:4px;background:#212121}
.item:hover{background:#2f2f2f;opacity:1}
.rtitle{font-size:11px;opacity:.5;margin-top:16px;display:flex;justify-content:space-between}
.clear-btn{background:#ff3333;color:#fff;border:none;padding:4px 8px;border-radius:6px;font-size:10px;cursor:pointer}
.rec-item{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;background:#2f2f2f;margin-bottom:5px;border-radius:8px}
.rec-text{font-size:12px;opacity:.7;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}
.main{flex:1;background:#212121;display:flex;flex-direction:column}
.top{padding:12px 16px;border-bottom:1px solid #333;display:flex;justify-content:space-between;font-weight:700}
.chat{flex:1;overflow:auto;padding:20px;max-width:850px;margin:0 auto;width:100%}
.msg{margin:14px 0;line-height:1.7;white-space:pre-wrap;word-wrap:break-word}
.assistant{background:#2f2f2f;padding:14px 16px;border-radius:16px}
.center{max-width:540px;margin:40px auto;display:flex;flex-direction:column;gap:8px;text-align:center}
.opt{opacity:.8;cursor:pointer;padding:12px;border-radius:12px;background:#2f2f2f;display:flex;gap:10px;text-align:left}
.opt:hover{opacity:1}
.box{max-width:850px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:12px 16px;gap:8px}
.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:15px}
.icon{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:.7}
.send{background:#fff;color:#000;width:34px;height:34px;border-radius:50%;border:none;cursor:pointer;font-weight:800}
.newchat{position:fixed;bottom:16px;left:16px;background:#3b82f6;color:#fff;border:none;padding:10px 18px;border-radius:24px;font-weight:600;cursor:pointer}
@media(max-width:768px){.side{display:none}}
</style></head><body>
<div class="side">
<div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍</span></div>
<div class="lang-box">
<div style="font-size:11px;opacity:.6">🌍 Bhasha</div>
<select id="langSel" onchange="saveLang()">
<option value="auto">Auto Detect</option><option value="te">Telugu తెలుగు</option><option value="en">English</option><option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option><option value="ml">Malayalam</option>
</select>
</div>
<div class="item" onclick="quick('create image lord rama full royal dress')">🖼️ Create Image - All Gods Traditional</div>
<div class="item" onclick="quickSearch()">🌐 Search the Web</div>
<div class="item" onclick="quick('Naku oka katha cheppu')">✏️ Kathalu & Writing</div>
<div class="item" onclick="quick('Translate to English: Ela unnavu?')">🌍 Translate</div>
<div class="item" onclick="quick('Python lo calculator code rayi')">💻 Code Help</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div>
<div id="rlist" style="margin-top:8px"></div>
</div>
<div class="main">
<div class="top"><div>✨ Andhariki-AI - Andariki Kosam</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:5px 12px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center">
<h3>Namaste babooie! Nenu Andhariki-AI 🙏</h3><p style="font-size:12px;opacity:.6">Adugu babooie - Chat, Image (All Gods Traditional Full Dress), Search, Code, Voice - Anni Chestha!</p>
<div class="opt" onclick="quick('create image lord rama full royal dress golden kurta')">🙏 Lord Rama - Full Dress</div>
<div class="opt" onclick="quick('create image lord krishna full royal dress kurta flute')">🦚 Lord Krishna - Full Dress</div>
<div class="opt" onclick="quick('create image lord shiva meditating full dress')">🔱 Lord Shiva - Full Dress</div>
<div class="opt" onclick="quick('create image lord ganesh traditional')">🐘 Lord Ganesh - Traditional</div>
<div class="opt" onclick="quick('create image goddess durga full saree')">🌺 Goddess Durga - Full Saree</div>
</div></div></div>
<div style="padding:14px"><div class="box">
<button class="icon" onclick="quick('create image ')">+</button>
<input id="inp" placeholder="Emaina adugu babooie..." onkeypress="if(event.key==='Enter')send()">
<button class="icon" onclick="startVoice()">🎤</button>
<button class="send" onclick="send()">↑</button>
</div><div style="text-align:center;font-size:10px;opacity:.25;margin-top:6px">Andhariki-AI - Made for Everyone ❤️ Traditional & Respectful</div></div>
</div>
<button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'auto';
document.getElementById('langSel').value=curLang;
let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel()}
function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🌍 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){let l=document.getElementById('rlist');l.innerHTML='';recents.slice(0,15).forEach((t,i)=>{let d=document.createElement('div');d.className='rec-item';d.innerHTML=`<span class=rec-text onclick="quick('${t.replace(/'/g," ")}')">${t.substring(0,35)}</span><span onclick='deleteOne(${i})' style=cursor:pointer>❌</span>`;l.appendChild(d)})}renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Anni delete cheyala babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>New Chat Started ✅</h3><p>Andhariki-AI Ready!</p></div>';history=[]}}
function newChat(){clearAll()}
function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}

async function send(){
 let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;
 let low=text.toLowerCase();
 if(low.includes('image')||low.includes('photo')||low.includes('rama')||low.includes('krishna')||low.includes('shiva')||low.includes('ganesh')||low.includes('hanuman')||low.includes('durga')||low.includes('lakshmi')||low.includes('venkateswara')||low.includes('ayyappa')||low.includes('sai')||low.includes('bommaru')){
  addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();inp.value='';
  let r=await fetch('/make_image_prompt?q='+encodeURIComponent(text));
  let d=await r.json();
  let prompt=d.prompt;
  addMsg('🎨 Andhariki-AI traditional image chestondi babooie...','assistant');
  let seed=Math.floor(Math.random()*999999);
  let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=768&model=flux&nologo=true&seed=${seed}&enhance=true`;
  let imgHTML=`<div style="margin-top:10px">Idigo babooie - 100% Traditional Full Dress - Jai Shree Ram 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download HD</a></div>`;
  setTimeout(()=>addMsg(imgHTML,'assistant'),900);
  return;
 }
 addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();
 history.push({role:'user',content:text});inp.value='';
 let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Andhariki-AI alochistondi...';document.getElementById('msgs').appendChild(ty);
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});
  let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});
 }catch(e){ty.textContent='Babooie, GROQ_API_KEY check chey Render lo!'}
}
function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}
async function quickSearch(){let q=prompt('Em search cheyali babooie?');if(!q)return;addMsg('Nuvvu: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}
</script></body></html>
    """

@app.route("/chat", methods=["POST"])
def chat_api():
    d=request.json
    return jsonify({"reply": ask_ai(d.get("history",[]), d.get("lang","auto"))})

@app.route("/make_image_prompt")
def make_image_prompt():
    q=request.args.get("q","")
    low=q.lower()
    for k,v in GOD_PROMPTS.items():
        if k in low:
            return jsonify({"prompt": v})
    clean = q.replace("create image","").replace("image","").replace("photo","").strip()[:60]
    final = f"{clean} wearing FULLY COVERED traditional Indian temple royal dress kurta dhoti saree chest fully covered NOT topless NOT bare chest modest divine 4k"
    return jsonify({"prompt": final})

@app.route("/search")
def search_route():
    q=request.args.get("q",""); lang=request.args.get("lang","auto")
    try:
        info=requests.get(f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json",timeout=8).json().get("AbstractText","")[:500]
        return jsonify({"result": ask_ai([{"role":"user","content":f"Search: {q}. Info: {info}. Answer helpfully."}], lang)})
    except:
        return jsonify({"result": ask_ai([{"role":"user","content":q}], lang)})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
