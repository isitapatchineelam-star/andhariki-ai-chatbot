from flask import Flask, request, jsonify
import os, requests, urllib.parse

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

# 100% TRADITIONAL TEMPLE PAINTING PROMPTS - RAJA RAVI VARMA STYLE
TRADITIONAL_GODS = {
"rama": "Lord Rama traditional Raja Ravi Varma oil painting style, ancient Indian temple mural, 25 years old handsome, wearing fully covered royal golden silk achkan kurta with high collar long sleeves chest fully covered, orange silk dhoti angavastram with golden border, golden kireeta mukut crown, pearl necklace, holding kodanda bow, Ayodhya palace background, ultra realistic traditional Indian painting, NOT topless NOT bare chest, respectful divine",
"krishna": "Lord Krishna traditional Raja Ravi Varma oil painting, ancient Vrindavan temple mural, blue skin divine, wearing fully covered golden silk achkan kurta high collar long sleeves chest fully covered, yellow silk dhoti orange angavastram, peacock feather golden mukut, pearl haram, playing wooden flute, lotus pond with peacocks, ultra realistic traditional painting, NOT topless NOT bare chest",
"shiva": "Lord Shiva traditional temple painting, Himalayan Kailash background, wearing fully covered tiger skin rudraksha mala tripundra on forehead, trishul damru, silk dhoti chest covered with vibhuti and rudraksha, meditating, ancient oil painting style, NOT topless, divine respectful",
"ganesh": "Lord Ganesha traditional Raja Ravi Varma painting, cute elephant head, wearing fully covered red and golden silk kurta dhoti, golden crown, four hands with modak pasha ankusha, temple background, traditional Indian oil painting realistic, divine",
"hanuman": "Lord Hanuman traditional temple mural painting, muscular vanara, wearing fully covered orange silk kurta dhoti, golden crown, holding gada mace, chest covered with sindoor, Himalayan background, ancient realistic painting, NOT topless",
"durga": "Goddess Durga Maa traditional Bengali temple painting Raja Ravi Varma style, wearing fully covered red silk saree with golden border, fully covered blouse chest fully covered, 10 hands with weapons, lion, golden crown, lotus, traditional realistic oil painting NOT revealing respectful",
"lakshmi": "Goddess Lakshmi traditional temple painting, wearing fully covered red silk saree golden blouse chest fully covered, golden crown, sitting on lotus holding lotus coins, elephants, ancient realistic painting respectful",
"saraswati": "Goddess Saraswati traditional painting, wearing fully covered white silk saree with golden border, fully covered blouse, veena book swan, ancient realistic oil painting divine",
"venkateswara": "Lord Venkateswara Tirupati Balaji traditional temple painting, wearing fully covered golden silk dhoti, golden crown tilak, chest covered with ornaments, ancient realistic South Indian temple style",
"ayyappa": "Lord Ayyappa Sabarimala traditional Kerala mural painting, wearing fully covered black dhoti golden ornaments, golden crown, chest covered, forest temple background, traditional realistic",
"saibaba": "Shirdi Sai Baba traditional painting, wearing fully covered white kafni long kurta chest fully covered, sitting in Dwarkamai, realistic old photo style divine"
}

def get_traditional_prompt(text):
    low=text.lower()
    for k,v in TRADITIONAL_GODS.items():
        if k in low:
            return v
    clean=text.replace("create image","").replace("image","").replace("bommaru","").replace("photo","").strip()[:60]
    return f"{clean} traditional Raja Ravi Varma oil painting style ancient Indian temple mural ultra realistic fully covered traditional silk dress kurta dhoti saree chest fully covered NOT topless NOT bare chest modest divine respectful 4k"

def ask_ai(history, lang="auto"):
    lang_instr = f"Reply ONLY in {lang} language. " if lang!="auto" else "Auto detect user language and reply same language. "
    msgs=[{"role":"system","content":f"You are Andhariki-AI Personal Assistant made by Andhariki Team. {lang_instr} You can do everything - coding, writing, translation, search, education, stories. Be helpful respectful. Call user babooie. Never say ChatGPT or OpenAI - you are Andhariki-AI only."}]
    for h in history[-15:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"openai/gpt-oss-20b","messages":msgs,"temperature":0.7,"max_tokens":2500},timeout=35)
        d=r.json()
        if "choices" in d: return d['choices'][0]['message']['content']
        return str(d)[:400]
    except Exception as e: return f"Error: {e}"

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
<div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍 Traditional</span></div>
<div class="lang-box">
<div style="font-size:11px;opacity:.6">🌍 Bhasha</div>
<select id="langSel" onchange="saveLang()">
<option value="auto">Auto Detect</option><option value="te">Telugu తెలుగు</option><option value="en">English</option><option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option><option value="ml">Malayalam</option>
</select>
</div>
<div class="item" onclick="quick('create image lord rama traditional temple painting')">🖼️ All Gods - Traditional Temple Style</div>
<div class="item" onclick="quickSearch()">🌐 Search the Web</div>
<div class="item" onclick="quick('Naku oka katha cheppu')">✏️ Kathalu</div>
<div class="item" onclick="quick('Translate to English: Ela unnavu?')">🌍 Translate</div>
<div class="item" onclick="quick('Python lo calculator code rayi')">💻 Code</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div>
<div id="rlist" style="margin-top:8px"></div>
</div>
<div class="main">
<div class="top"><div>✨ Andhariki-AI - Traditional & Divine</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:5px 12px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center">
<h3>Namaste babooie! Nenu Andhariki-AI 🙏</h3><p style="font-size:12px;opacity:.6">Traditional Temple Paintings - Raja Ravi Varma Style lo Gods vastaru!</p>
<div class="opt" onclick="quick('create image lord rama traditional temple painting raja ravi varma style')">🙏 Rama - Temple Painting</div>
<div class="opt" onclick="quick('create image lord krishna traditional raja ravi varma vrindavan')">🦚 Krishna - Temple Painting</div>
<div class="opt" onclick="quick('create image lord shiva traditional kailash')">🔱 Shiva - Temple Painting</div>
<div class="opt" onclick="quick('create image lord ganesh traditional')">🐘 Ganesh - Traditional</div>
<div class="opt" onclick="quick('create image goddess durga traditional red saree')">🌺 Durga - Traditional Saree</div>
</div></div></div>
<div style="padding:14px"><div class="box">
<button class="icon" onclick="quick('create image ')">+</button>
<input id="inp" placeholder="Emaina adugu babooie..." onkeypress="if(event.key==='Enter')send()">
<button class="icon" onclick="startVoice()">🎤</button>
<button class="send" onclick="send()">↑</button>
</div><div style="text-align:center;font-size:10px;opacity:.25;margin-top:6px">Andhariki-AI - Traditional Temple Style - Made with Love ❤️</div></div>
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
function clearAll(){if(confirm('Anni delete cheyala babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>New Chat Started ✅</h3><p>Andhariki-AI Traditional Ready!</p></div>';history=[]}}
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
  addMsg('🎨 Andhariki-AI traditional temple painting chestondi...','assistant');
  let seed=Math.floor(Math.random()*999999);
  // TRADITIONAL MODEL - more realistic traditional
  let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=768&model=flux&nologo=true&seed=${seed}&enhance=true`;
  let imgHTML=`<div style="margin-top:10px">Idigo babooie - 100% Traditional Temple Style 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download HD</a></div>`;
  setTimeout(()=>addMsg(imgHTML,'assistant'),900);
  return;
 }
 addMsg('Nuvvu: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();
 history.push({role:'user',content:text});inp.value='';
 let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Andhariki-AI alochistondi...';document.getElementById('msgs').appendChild(ty);
 try{
  let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});
  let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});
 }catch(e){ty.textContent='GROQ_API_KEY check chey babooie!'}
}
function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}
async function quickSearch(){let q=prompt('Em search cheyali?');if(!q)return;addMsg('Nuvvu: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}
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
    for k,v in TRADITIONAL_GODS.items():
        if k in low:
            return jsonify({"prompt": v})
    clean = q.replace("create image","").replace("image","").replace("bommaru","").strip()[:60]
    final = f"{clean} traditional Raja Ravi Varma oil painting ancient Indian temple mural ultra realistic fully covered silk kurta dhoti saree chest fully covered NOT topless modest divine respectful 4k"
    return jsonify({"prompt": final})

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
