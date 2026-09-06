from flask import Flask, request, jsonify
import os, requests, urllib.parse
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

def ask_groq(history, lang="auto"):
    lang_instr = f"Reply ONLY in {lang}. " if lang!="auto" else "Auto detect language and reply same. "
    msgs=[{"role":"system","content":f"You are Andhariki-AI Personal Assistant. {lang_instr} You are ChatGPT clone - answer everything like ChatGPT, coding, writing, stories. Call user babooie."}]
    for h in history[-10:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"openai/gpt-oss-20b","messages":msgs,"temperature":0.7},timeout=30)
        data=r.json()
        return data['choices'][0]['message']['content'] if "choices" in data else str(data)
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
.logo{font-weight:700;font-size:18px}.logo span{font-size:11px;opacity:0.5}
.lang-box{margin:12px 0;background:#2f2f2f;padding:10px;border-radius:10px}
.lang-box select{width:100%;background:#212121;color:#fff;border:1px solid #444;padding:8px;border-radius:8px;margin-top:6px}
.item{padding:9px;border-radius:8px;opacity:0.7;font-size:13px;cursor:pointer;display:flex;gap:10px;margin-bottom:2px}
.item:hover{background:#2f2f2f;opacity:1}
.rtitle{font-size:11px;opacity:0.5;margin-top:14px;display:flex;justify-content:space-between}
.clear-btn{background:#ff3333;color:#fff;border:none;padding:4px 8px;border-radius:6px;font-size:10px;cursor:pointer}
.rec-item{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;background:#2f2f2f;margin-bottom:5px;border-radius:8px}
.rec-text{font-size:12px;opacity:0.7;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.main{flex:1;background:#212121;display:flex;flex-direction:column}
.top{padding:10px 14px;border-bottom:1px solid #333;display:flex;justify-content:space-between}
.chat{flex:1;overflow:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:14px 0;line-height:1.7;white-space:pre-wrap;word-wrap:break-word}
.assistant{background:#2f2f2f;padding:12px 14px;border-radius:14px}
.center{max-width:520px;margin:50px auto;display:flex;flex-direction:column;gap:8px}
.opt{opacity:0.6;cursor:pointer;padding:8px;border-radius:8px;background:#2f2f2f;display:flex;gap:10px;text-align:left}
.opt:hover{opacity:1}
.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:10px 14px;gap:8px}
.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:15px}
.icon{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:0.7}
.send{background:#fff;color:#000;width:32px;height:32px;border-radius:50%;border:none;cursor:pointer;font-weight:700}
.newchat{position:fixed;bottom:16px;left:16px;background:#3b82f6;color:#fff;border:none;padding:10px 16px;border-radius:24px;font-weight:600;cursor:pointer}
@media(max-width:768px){.side{display:none}}
</style></head><body>
<div class="side">
<div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍</span></div>
<div class="lang-box">
<div style="font-size:11px;opacity:0.6">🌍 Language</div>
<select id="langSel" onchange="saveLang()">
<option value="auto">Auto Detect</option>
<option value="te">Telugu తెలుగు</option><option value="en">English</option>
<option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option>
<option value="ml">Malayalam</option><option value="ur">Urdu</option>
<option value="mr">Marathi</option><option value="bn">Bengali</option>
<option value="es">Spanish</option><option value="fr">French</option>
</select>
</div>
<div class="item" onclick="quick('create image lord rama')">🖼️ Create Image</div>
<div class="item" onclick="quickSearch()">🌐 Search the web</div>
<div class="item" onclick="quick('Write a love story in Telugu')">✏️ Write or edit</div>
<div class="item" onclick="quick('Translate to Hindi: How are you?')">🌍 Translate</div>
<div class="item" onclick="quick('Write python code for calculator')">💻 Code Help</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div>
<div id="rlist" style="margin-top:8px"></div>
</div>
<div class="main">
<div class="top"><div>✨ Andhariki-AI Personal Assistant</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:4px 10px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center">
<h3>Andhariki-AI ChatGPT Clone 🌍</h3><p style="font-size:12px;opacity:0.6">Ask anything - All features like ChatGPT</p>
<div class="opt" onclick="quick('create image lord rama royal king')">🖼️ Lord Rama - Royal Dress</div>
<div class="opt" onclick="quick('create image lord krishna flute')">🖼️ Lord Krishna</div>
<div class="opt" onclick="quick('What is Java? Explain in Telugu')">💬 What is Java?</div>
<div class="opt" onclick="quick('Write python code for calculator')">💻 Write Code</div>
</div></div></div>
<div style="padding:14px"><div class="box">
<button class="icon" onclick="quick('create image ')">+</button>
<input id="inp" placeholder="Ask anything like ChatGPT..." onkeypress="if(event.key==='Enter')send()">
<button class="icon" onclick="startVoice()">🎤</button>
<button class="send" onclick="send()">↑</button>
</div><div style="text-align:center;font-size:10px;opacity:0.3;margin-top:6px">ChatGPT features - Image, Search, Write, Translate, Code, Voice, History</div></div>
</div>
<button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'auto';
document.getElementById('langSel').value=curLang;
let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel()}
function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🌍 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){let l=document.getElementById('rlist');l.innerHTML='';recents.forEach((t,i)=>{let d=document.createElement('div');d.className='rec-item';d.innerHTML=`<span class=rec-text>${t}</span><span onclick='deleteOne(${i})' style=cursor:pointer>❌</span>`;l.appendChild(d)})}renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Delete all history babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3>History Cleared ✅</h3></div>';history=[]}}
function newChat(){clearAll()}
function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}

async function send(){
 let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;
 let low=text.toLowerCase();
 // IMAGE - SHORT PROMPT FIX FOR YOUR ERROR
 if(low.includes('image')||low.includes('photo')||low.includes('rama')||low.includes('krishna')||low.includes('shiva')||low.includes('ganesh')||low.includes('hanuman')){
  addMsg('You: '+text,'user');
  recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();
  inp.value='';
  let prompt='lord rama';
  if(low.includes('rama')) prompt='Lord Rama royal king orange dhoti crown bow';
  else if(low.includes('krishna')) prompt='Lord Krishna blue skin peacock feather flute';
  else if(low.includes('shiva')) prompt='Lord Shiva trishul meditating';
  else if(low.includes('ganesh')) prompt='Lord Ganesha cute elephant god';
  else if(low.includes('hanuman')) prompt='Lord Hanuman powerful monkey god';
  else prompt=text.replace(/create image|create a image|image|photo|picture/gi,'').trim().substring(0,60);

  addMsg('🎨 Creating "'+prompt+'" babooie...','assistant');
  let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=512&nologo=true&seed=${Math.floor(Math.random()*9999)}`;
  let imgTag=`<div style="margin-top:10px">Here babooie! 🙏<br><img src="${url}" style="width:100%;max-width:512px;border-radius:12px;margin-top:8px;border:1px solid #444"><br><a href="${url}" target="_blank" style="color:#5da8ff;font-size:12px">📥 Download</a></div>`;
  setTimeout(()=>addMsg(imgTag,'assistant'),700);
  return;
 }
 addMsg('You: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();
 history.push({role:'user',content:text});inp.value='';
 let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Thinking...';document.getElementById('msgs').appendChild(ty);
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});
 let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});
}
function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN','ml':'ml-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}
async function quickSearch(){let q=prompt('Search what babooie?');if(!q)return;addMsg('You: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}
</script></body></html>
    """

@app.route("/chat", methods=["POST"])
def chat_api():
    d=request.json
    return jsonify({"reply": ask_groq(d.get("history",[]), d.get("lang","auto"))})

@app.route("/search")
def search_route():
    q=request.args.get("q",""); lang=request.args.get("lang","auto")
    try:
        info=requests.get(f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json",timeout=8).json().get("AbstractText","")
        return jsonify({"result": ask_groq([{"role":"user","content":f"Search {q}. Info: {info}"}], lang)})
    except:
        return jsonify({"result": ask_groq([{"role":"user","content":q}], lang)})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
