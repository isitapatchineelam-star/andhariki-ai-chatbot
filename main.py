from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY", "").strip()

def ask_groq(history):
    if not GROQ_KEY:
        return "⚠️ Render lo GROQ_API_KEY ledu babooie! Groq.com nundi key techi Environment lo pettali."

    try:
        msgs = [
            {"role":"system","content":"You are Andhariki AI - Personal Assistant like ChatGPT. You are friendly, helpful. Answer in Telugu + English mix, call user babooie. Give real, detailed, helpful answers like ChatGPT."}
        ]
        # last 8 messages memory
        for h in history[-8:]:
            if h.get('role') in ['user','assistant']:
                msgs.append({"role": h['role'], "content": h['content']})

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
            json={
                "model":"llama-3.3-70b-versatile",
                "messages": msgs,
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=30)

        data = r.json()

        if "choices" not in data:
            err = data.get("error", {}).get("message", str(data)[:300])
            return f"Groq Error: {err}"

        return data['choices'][0]['message']['content']

    except Exception as e:
        return f"Error: {e}"

HTML = """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Andhariki AI - Personal Assistant</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#212121;color:#ececec;font-family:Inter,system-ui,sans-serif;display:flex;height:100vh;overflow:hidden}
.side{width:260px;background:#171717;padding:12px;display:flex;flex-direction:column;gap:10px;border-right:1px solid #333}
.side button{width:100%;background:#2f2f2f;border:1px solid #444;color:#fff;padding:12px;border-radius:10px;cursor:pointer;text-align:left;font-size:14px}
.side button:hover{background:#3f3f3f}
.hist{flex:1;overflow-y:auto;font-size:13px;margin-top:10px}
.main{flex:1;display:flex;flex-direction:column;background:#212121;overflow:hidden}
.top{padding:14px;text-align:center;border-bottom:1px solid #333;font-weight:600;font-size:15px;background:#212121}
.chat{flex:1;overflow-y:auto;padding:24px;max-width:850px;margin:0 auto;width:100%}
.msg{margin:20px 0;line-height:1.7;white-space:pre-wrap;word-wrap:break-word}
.msg.you{font-weight:500}
.msg.ai{opacity:0.95}
.area{padding:16px 20px;background:#212121;border-top:1px solid #333}
.box{max-width:850px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;padding:12px 16px;gap:10px;align-items:center;border:1px solid #444}
.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:16px}
.send{background:#fff;color:#000;width:36px;height:36px;border-radius:50%;border:none;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center}
@media(max-width:700px){.side{display:none}}
</style></head><body>
<div class="side">
<button onclick="newChat()">+ New Chat</button>
<div class="hist" id="hist"></div>
<p style="font-size:11px;opacity:0.4;margin-top:auto">Andhariki AI v2 - ChatGPT Clone</p>
</div>
<div class="main">
<div class="top">Andhariki AI - Personal Assistant</div>
<div class="chat" id="chat"><div id="messages"><div style="text-align:center;margin-top:18%;opacity:0.7">
<h2>Andhariki AI Ready! 🚀</h2><p>ChatGPT la ye question aina adugu babooie!</p><p style="font-size:13px">Python, Wife tips, Jobs - anni vastayi!</p>
</div></div></div>
<div class="area">
<div class="box">
<input id="inp" placeholder="Message Andhariki AI..." onkeypress="if(event.key==='Enter')send()">
<button class="send" onclick="send()">↑</button>
</div>
</div>
</div>
<script>
let msgsEl=document.getElementById('messages'), chatEl=document.getElementById('chat'), inp=document.getElementById('inp');
let history=[];
function newChat(){history=[];msgsEl.innerHTML='<div style="text-align:center;margin-top:18%;opacity:0.7"><h2>Andhariki AI Ready! 🚀</h2><p>Ye question aina adugu babooie!</p></div>';}
function addMsg(role,text){
  if(msgsEl.innerHTML.includes('Ready!')) msgsEl.innerHTML='';
  let d=document.createElement('div'); d.className='msg '+(role==='user'?'you':'ai');
  d.textContent = (role==='user'? 'You: ' : 'Andhariki AI: ') + text;
  msgsEl.appendChild(d); chatEl.scrollTop=chatEl.scrollHeight+200;
}
async function send(){
  let text=inp.value.trim(); if(!text) return;
  addMsg('user',text); history.push({role:'user',content:text}); inp.value='';
  let typing=document.createElement('div'); typing.className='msg ai'; typing.textContent='Andhariki AI typing...'; msgsEl.appendChild(typing);
  chatEl.scrollTop=chatEl.scrollHeight+200;
  try{
    let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history})});
    let data=await r.json(); typing.remove();
    addMsg('assistant',data.reply); history.push({role:'assistant',content:data.reply});
  }catch(e){ typing.textContent='Error: '+e; }
}
</script>
</body></html>"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat_api():
    history = request.json.get("history", [])
    ans = ask_groq(history)
    return jsonify({"reply": ans})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
