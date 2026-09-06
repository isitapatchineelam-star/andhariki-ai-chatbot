from flask import Flask, request, jsonify
import os, requests, json
from datetime import datetime

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

def ask_groq(history):
    # ChatGPT la model - Llama 3
    if not GROQ_KEY:
        return "⚠️ Groq Key ledu babooie! Render lo GROQ_API_KEY add chey. Lekapote na local answer istanu."
    try:
        msgs = [{"role":"system","content":"You are Andhariki AI - Personal Assistant like ChatGPT. Answer in Telugu+English mix, friendly as babooie. Ye question aina real, helpful answer ivvu. User ni babooie ani piluvu."}]
        for h in history[-10:]: # last 10 msgs memory
            msgs.append(h)
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":msgs,"temperature":0.7},
            timeout=20)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Groq error: {e} - kani nenu unna! Adugu malli."

HTML = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki AI - Personal Assistant</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#212121;color:#ececec;font-family:Inter,sans-serif;display:flex;height:100vh}
.side{width:260px;background:#171717;padding:12px;display:flex;flex-direction:column;gap:10px}
.side button{width:100%;background:transparent;border:1px solid #333;color:#fff;padding:12px;border-radius:10px;cursor:pointer;text-align:left}
.side button.new{background:#2f2f2f}.hist{flex:1;overflow-y:auto;font-size:13px}.hist div{padding:8px;border-radius:8px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.hist div:hover{background:#2a2a2a}
.main{flex:1;display:flex;flex-direction:column;background:#212121}.top{padding:12px;text-align:center;border-bottom:1px solid #333;font-weight:600}
.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}.msg{margin:16px 0;display:flex;gap:12px;line-height:1.7;white-space:pre-wrap}.msg.user{justify-content:flex-end}.bubble{max-width:85%;padding:12px 16px;border-radius:18px}.user.bubble{background:#2f2f2f}.ai.bubble{background:transparent}
.area{padding:16px;background:#212121}.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;padding:10px 14px;gap:8px}.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:16px}.send{background:#fff;color:#000;width:36px;height:36px;border-radius:50%;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
@media(max-width:700px){.side{display:none}}
</style></head><body>
<div class=side>
<button class=new onclick="newChat()">+ New Chat</button>
<button onclick="clearAll()">🗑️ Clear History</button>
<div class=hist id=hist></div>
</div>
<div class=main>
<div class=top>Andhariki AI - Personal Assistant</div>
<div class=chat id=chat><div id=messages></div></div>
<div class=area><div class=box><input id=inp placeholder="Message Andhariki AI..." onkeypress="if(event.key==='Enter')send()"><button class=send onclick=send()>↑</button></div></div>
</div>
<script>
let msgs=document.getElementById('messages'), chat=document.getElementById('chat'), inp=document.getElementById('inp'), histDiv=document.getElementById('hist');
let allChats=JSON.parse(localStorage.getItem('all_chats')||'{}'), curId=localStorage.getItem('cur_id')||Date.now().toString();
function save(){localStorage.setItem('all_chats',JSON.stringify(allChats));localStorage.setItem('cur_id',curId);renderHist()}
function renderHist(){histDiv.innerHTML='';Object.keys(allChats).reverse().forEach(id=>{let t=allChats[id][0]?.content?.slice(0,30)||'New Chat';let d=document.createElement('div');d.textContent=t;d.onclick=()=>{curId=id;loadChat()};histDiv.appendChild(d)})}
function loadChat(){let h=allChats[curId]||[];msgs.innerHTML='';if(!h.length){msgs.innerHTML='<div style=text-align:center;margin-top:20%;opacity:0.6><h2>Andhariki AI - Personal Assistant</h2><p>ChatGPT la ye question aina adugu babooie 🌍</p></div>'}else{h.forEach(x=>{if(x.role!=='system')addMsg(x.content,x.role)}); }chat.scrollTop=99999;renderHist()}
function newChat(){curId=Date.now().toString();allChats[curId]=[];save();loadChat()}
function clearAll(){if(confirm('History motham clear cheyala?')){allChats={};newChat()}}
function addMsg(t,role){let d=document.createElement('div');d.className='msg '+(role==='user'?'user':'ai');d.innerHTML=`<div class=bubble>${t.replace(/</g,'&lt;')}</div>`;msgs.appendChild(d);chat.scrollTop=99999}
window.onload=loadChat;
async function send(){let text=inp.value.trim();if(!text)return;if(msgs.innerHTML.includes('Andhariki AI - Personal'))msgs.innerHTML='';addMsg(text,'user');inp.value='';if(!allChats[curId])allChats[curId]=[];allChats[curId].push({role:'user',content:text});save();let typing=document.createElement('div');typing.className='msg ai';typing.innerHTML='<div class=bubble>...</div>';msgs.appendChild(typing);chat.scrollTop=99999;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:allChats[curId]})});let data=await r.json();typing.remove();addMsg(data.reply,'assistant');allChats[curId].push({role:'assistant',content:data.reply});save()}
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/chat", methods=["POST"])
def chat_api():
    history = request.json.get("history", [])
    # Last message
    last_q = history[-1]['content'] if history else ""
    # If no groq key, give smart local
    if not GROQ_KEY:
        low=last_q.lower()
        if "wife" in low: return jsonify({"reply":"💖 Wife ni impress: 1. Chinna gift 2. Help 3. Vinu 4. Compliment 5. Time ivvu - Groq key add cheste inka deep answer istanu babooie!"})
        return jsonify({"reply": f"🌍 '{last_q}' ki answer - Groq API key Render lo add chey babooie, apudu ChatGPT la world knowledge vastadi! Key lekunda kuda nenu basic answer istanu."})
    ans = ask_groq(history)
    return jsonify({"reply": ans})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
