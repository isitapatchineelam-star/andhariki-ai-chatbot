from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY","").strip()

def ask_groq(history):
    msgs=[{"role":"system","content":"You are Andhariki AI, like ChatGPT. Friendly Telugu+English, call user babooie. Give detailed helpful answers."}]
    for h in history[-8:]:
        if h.get('role') in ['user','assistant']: msgs.append(h)
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},json={"model":"openai/gpt-oss-20b","messages":msgs},timeout=30)
        data=r.json()
        if "choices" not in data: return f"Error: {data.get('error',{}).get('message','')}"
        return data['choices'][0]['message']['content']
    except Exception as e: return f"Error: {e}"

HTML = """
<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,sans-serif}
body{background:#000;color:#fff;display:flex;height:100vh;overflow:hidden}
.side{width:280px;background:#171717;display:flex;flex-direction:column;padding:12px;transition:0.3s}
.side-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.logo{font-size:22px;font-weight:600}
.menu-item{display:flex;align-items:center;gap:14px;padding:10px 12px;border-radius:8px;opacity:0.8;cursor:pointer}
.menu-item:hover{background:#2f2f2f}
.recents{margin-top:24px;flex:1;overflow:auto}
.recents-title{font-size:13px;opacity:0.5;margin-bottom:10px;padding-left:12px}
.recent-item{padding:8px 12px;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:0.7;border-radius:8px;cursor:pointer}
.recent-item:hover{background:#2f2f2f}
.main{flex:1;display:flex;flex-direction:column;background:#212121;position:relative}
.topbar{padding:14px;text-align:center;border-bottom:1px solid #333;font-weight:600}
.chat{flex:1;overflow:auto;padding:24px;max-width:800px;margin:0 auto;width:100%}
.msg{margin:18px 0;line-height:1.7;white-space:pre-wrap}
.user{opacity:0.9}
.assistant{background:#2f2f2f;padding:14px 16px;border-radius:16px}
.bottom{padding:16px;background:linear-gradient(transparent,#212121)}
.input-box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;align-items:center;padding:8px 14px;gap:10px}
.input-box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:16px}
.send-btn{width:32px;height:32px;border-radius:50%;background:#fff;color:#000;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer}
.new-chat-btn{position:fixed;bottom:20px;left:20px;background:#3b82f6;color:#fff;border:none;padding:12px 20px;border-radius:28px;display:flex;gap:8px;align-items:center;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.5)}
.hamburger{display:none}
@media(max-width:768px){.side{position:fixed;left:-100%;z-index:99;height:100vh}.side.open{left:0}.hamburger{display:block;position:absolute;left:14px;top:14px;background:#2f2f2f;border:none;color:#fff;width:36px;height:36px;border-radius:50%}}
</style></head><body>
<div class="side" id="side">
<div class="side-top"><div class="logo">Andhariki AI</div><button onclick="toggleSide()" style="background:transparent;border:none;color:#fff;font-size:20px">✕</button></div>
<div class="menu-item"><span>🖼️</span> Images</div>
<div class="menu-item"><span>📚</span> Library</div>
<div class="menu-item"><span>📁</span> Projects</div>
<div class="menu-item"><span>⏰</span> Scheduled</div>
<div class="menu-item"><span>@</span> Plugins</div>
<div class="recents"><div class="recents-title">Recents</div><div id="recentList"></div></div>
</div>
<div class="main">
<button class="hamburger" onclick="toggleSide()">☰</button>
<div class="topbar">Andhariki AI - Personal Assistant</div>
<div class="chat" id="chat"><div id="msgs"><div style="text-align:center;margin-top:20%;opacity:0.6"><h2>What can I help with babooie?</h2></div></div></div>
<div class="bottom"><div class="input-box"><input id="inp" placeholder="Message Andhariki AI..." onkeypress="if(event.key==='Enter')send()"><button class="send-btn" onclick="send()">↑</button></div></div>
</div>
<button class="new-chat-btn" onclick="newChat()"><span>📝</span> Chat</button>
<script>
let msgs=document.getElementById('msgs'), recentList=document.getElementById('recentList'), history=[];
let recents=JSON.parse(localStorage.getItem('recents')||'[]');
function renderRecents(){recentList.innerHTML='';recents.slice(0,10).forEach(t=>{let d=document.createElement('div');d.className='recent-item';d.textContent=t;recentList.appendChild(d)})}
renderRecents();
function toggleSide(){document.getElementById('side').classList.toggle('open')}
function newChat(){msgs.innerHTML='<div style=text-align:center;margin-top:20%;opacity:0.6><h2>What can I help with babooie?</h2></div>';history=[];toggleSide()}
function addMsg(text,cls){if(msgs.innerHTML.includes('What can I help'))msgs.innerHTML='';let d=document.createElement('div');d.className='msg '+cls;d.textContent=text;msgs.appendChild(d);document.getElementById('chat').scrollTop=99999}
async function send(){let inp=document.getElementById('inp');let text=inp.value.trim();if(!text)return;addMsg('You: '+text,'user');if(!recents.includes(text)){recents.unshift(text);localStorage.setItem('recents',JSON.stringify(recents.slice(0,20)));renderRecents()}history.push({role:'user',content:text});inp.value='';let typing=document.createElement('div');typing.className='msg assistant';typing.textContent='Andhariki AI is typing...';msgs.appendChild(typing);let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history})});let data=await r.json();typing.remove();addMsg(data.reply,'assistant');history.push({role:'assistant',content:data.reply})}
</script></body></html>
"""
@app.route("/")
def home(): return HTML
@app.route("/chat", methods=["POST"])
def chat_api(): return jsonify({"reply": ask_groq(request.json.get("history",[]))})
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
