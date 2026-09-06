from flask import Flask, request, jsonify
import os, requests, urllib.parse
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

def ask_groq(history, lang="auto"):
    lang_instr = f"Reply ONLY in {lang} language. " if lang!="auto" else "Auto detect user language and reply in same language. "
    msgs=[{"role":"system","content":f"You are Andhariki-AI Personal Assistant. {lang_instr} Support ALL languages. Call user babooie. Friendly like ChatGPT."}]
    for h in history[-8:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"openai/gpt-oss-20b","messages":msgs},timeout=30)
        data=r.json()
        return data['choices'][0]['message']['content'] if "choices" in data else f"Error: {data}"
    except Exception as e: return f"Error: {e}"

@app.route("/")
def home():
    return """
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>Andhariki-AI Personal Assistant</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#000;color:#fff;display:flex;height:100vh}
.side{width:280px;background:#171717;padding:14px;display:flex;flex-direction:column;overflow:auto}
.logo{font-weight:700;font-size:18px}.logo span{font-size:11px;opacity:0.5}
.lang-box{margin:14px 0;background:#2f2f2f;padding:10px;border-radius:10px}
.lang-box select{width:100%;background:#212121;color:#fff;border:1px solid #444;padding:8px;border-radius:8px;margin-top:6px}
.item{padding:9px;border-radius:8px;opacity:0.7;font-size:13px;cursor:pointer;display:flex;gap:10px}
.item:hover{background:#2f2f2f}
.rtitle{font-size:11px;opacity:0.4;margin-top:16px;display:flex;justify-content:space-between;align-items:center}
.main{flex:1;background:#212121;display:flex;flex-direction:column}
.top{padding:10px 14px;border-bottom:1px solid #333;display:flex;justify-content:space-between}
.chat{flex:1;overflow:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:14px 0;line-height:1.7;white-space:pre-wrap}
.assistant{background:#2f2f2f;padding:12px 14px;border-radius:14px}
.center{max-width:500px;margin:40px auto;display:flex;flex-direction:column;gap:10px}
.opt{opacity:0.6;cursor:pointer;padding:6px;display:flex;gap:10px}
.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:10px 14px;gap:8px}
.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:15px}
.icon{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer}
.send{background:#fff;color:#000;width:32px;height:32px;border-radius:50%;border:none;cursor:pointer}
.clear-btn{background:#ff3333;color:#fff;border:none;padding:5px 10px;border-radius:6px;font-size:10px;cursor:pointer}
.rec-item{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;background:#2f2f2f;margin-bottom:5px;border-radius:8px}
.rec-text{font-size:12px;opacity:0.7;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.del{cursor:pointer;margin-left:8px}
.newchat{position:fixed;bottom:16px;left:16px;background:#3b82f6;color:#fff;border:none;padding:10px 16px;border-radius:24px}
</style></head><body>
<div class="side">
<div class="logo">Andhariki-AI<br><span>Personal Assistant 🌍</span></div>
<div class="lang-box">
<div style="font-size:12px;opacity:0.6">🌍 Language</div>
<select id="langSel" onchange="saveLang()">
<option value="auto">Auto Detect</option><option value="te">Telugu</option><option value="en">English</option>
<option value="hi">Hindi</option><option value="ta">Tamil</option><option value="kn">Kannada</option>
<option value="ml">Malayalam</option><option value="ur">Urdu</option><option value="mr">Marathi</option>
<option value="bn">Bengali</option><option value="es">Spanish</option><option value="fr">French</option>
<option value="de">German</option><option value="ar">Arabic</option><option value="ja">Japanese</option>
</select>
</div>
<div class="item" onclick="quick('Create an image of ')">🖼️ Create image</div>
<div class="item" onclick="quickSearch()">🌐 Search web</div>
<div class="item" onclick="quick('Write: ')">✏️ Write or edit</div>
<div class="rtitle"><span>Recents</span><button class="clear-btn" onclick="clearAll()">Clear All</button></div>
<div id="rlist" style="margin-top:8px"></div>
</div>
<div class="main">
<div class="top"><div>✨ Andhariki-AI Personal Assistant</div><div id="curLang" style="font-size:11px;background:#2f2f2f;padding:4px 10px;border-radius:12px">🌍 Auto</div></div>
<div class="chat" id="chat"><div id="msgs"><div id="centerBox" class="center">
<div style="text-align:center;opacity:0.7"><h3>Andhariki-AI 🌍</h3><p style="font-size:12px">All Languages + Delete History</p></div>
<div class="opt" onclick="quick('Create an image of ')">🖼️ Create an image</div>
<div class="opt" onclick="quickSearch()">🌐 Search the web</div>
<div class="opt" onclick="quick('Write a story in Telugu: ')">✏️ Write in any language</div>
</div></div></div>
<div style="padding:14px"><div class="box">
<button class="icon" onclick="quick('Create image: ')">+</button>
<input id="inp" placeholder="Ask in any language..." onkeypress="if(event.key==='Enter')send()">
<button class="icon" onclick="startVoice()">🎤</button>
<button class="send" onclick="send()">↑</button>
</div></div>
</div>
<button class="newchat" onclick="newChat()">📝 New Chat</button>
<script>
let history=[], curLang=localStorage.getItem('andhariki_lang')||'auto';
document.getElementById('langSel').value=curLang;
let recents=JSON.parse(localStorage.getItem('andhariki_rec')||'[]');
function saveLang(){curLang=document.getElementById('langSel').value;localStorage.setItem('andhariki_lang',curLang);updateLabel()}
function updateLabel(){let s=document.getElementById('langSel');document.getElementById('curLang').textContent='🌍 '+s.options[s.selectedIndex].text}updateLabel();
function renderR(){
 let l=document.getElementById('rlist');l.innerHTML='';
 recents.forEach((t,i)=>{
  let div=document.createElement('div');div.className='rec-item';
  div.innerHTML=`<span class='rec-text'>${t}</span><span class='del' onclick='deleteOne(${i})'>❌</span>`;
  l.appendChild(div);
 });
}
renderR();
function deleteOne(i){recents.splice(i,1);localStorage.setItem('andhariki_rec',JSON.stringify(recents));renderR()}
function clearAll(){if(confirm('Delete all history babooie?')){recents=[];localStorage.removeItem('andhariki_rec');renderR();document.getElementById('msgs').innerHTML='<div id=centerBox class=center><h3 style=text-align:center;opacity:0.6>History Cleared ✅</h3></div>';history=[]}}
function newChat(){clearAll()}
function quick(t){document.getElementById('inp').value=t;document.getElementById('inp').focus()}
function addMsg(t,c){let cb=document.getElementById('centerBox');if(cb)cb.style.display='none';let d=document.createElement('div');d.className='msg '+c;d.innerHTML=t;document.getElementById('msgs').appendChild(d);document.getElementById('chat').scrollTop=999999}
async function send(){
 let inp=document.getElementById('inp'), text=inp.value.trim();if(!text)return;
 if(text.toLowerCase().includes('create image')){
  addMsg('You: '+text,'user');inp.value='';let p=encodeURIComponent(text.replace(/create image:?/gi,'').trim());
  addMsg(`<img src="https://image.pollinations.ai/prompt/${p}?nologo=true" style="width:100%;border-radius:12px">`,'assistant');return;
 }
 addMsg('You: '+text,'user');recents.unshift(text);localStorage.setItem('andhariki_rec',JSON.stringify(recents.slice(0,20)));renderR();
 history.push({role:'user',content:text});inp.value='';
 let ty=document.createElement('div');ty.className='msg assistant';ty.textContent='Thinking...';document.getElementById('msgs').appendChild(ty);
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history,lang:curLang})});
 let data=await r.json();ty.remove();addMsg(data.reply.replace(/\\n/g,'<br>'),'assistant');history.push({role:'assistant',content:data.reply});
}
function startVoice(){let m={'te':'te-IN','hi':'hi-IN','ta':'ta-IN','kn':'kn-IN'};let l=m[curLang]||'en-US';let rec=new (window.SpeechRecognition||window.webkitSpeechRecognition)();rec.lang=l;rec.onresult=e=>{document.getElementById('inp').value=e.results[0][0].transcript;send()};rec.start()}
async function quickSearch(){let q=prompt('Search what?');if(!q)return;addMsg('You: Search '+q,'user');let r=await fetch('/search?q='+encodeURIComponent(q)+'&lang='+curLang);let d=await r.json();addMsg(d.result,'assistant')}
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
