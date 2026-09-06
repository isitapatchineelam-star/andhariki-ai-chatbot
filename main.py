from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY", "").strip()

def ask_groq(history):
    if not GROQ_KEY:
        return "⚠️ GROQ_API_KEY ledu babooie! Render > Environment lo pettu."

    try:
        msgs = [{"role":"system","content":"You are Andhariki AI - Personal Assistant like ChatGPT. Friendly Telugu+English mix, call user babooie. Give detailed helpful answers."}]
        for h in history[-8:]:
            if h.get('role') in ['user','assistant']:
                msgs.append({"role": h['role'], "content": h['content']})

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
            json={
                "model":"openai/gpt-oss-20b",
                "messages": msgs,
                "temperature": 0.7
            },
            timeout=30)

        data = r.json()
        print(data)

        if "choices" not in data:
            # try 2nd model if first fails
            if "openai/gpt-oss-20b" in str(data):
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
                    json={"model":"llama-3.1-8b-instant","messages": msgs},
                    timeout=30)
                data = r.json()

            if "choices" not in data:
                return f"Groq Error: {data.get('error',{}).get('message',str(data)[:400])}"

        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

HTML = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki AI</title>
<style>body{margin:0;background:#212121;color:#ececec;font-family:sans-serif;display:flex;height:100vh}.side{width:260px;background:#171717;padding:12px}.main{flex:1;display:flex;flex-direction:column}.top{padding:12px;text-align:center;border-bottom:1px solid #333}.chat{flex:1;overflow:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}.msg{margin:16px 0;white-space:pre-wrap;line-height:1.6}.area{padding:16px}.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;padding:10px 14px;gap:8px}.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:16px}.send{background:#fff;color:#000;width:32px;height:32px;border-radius:50%;border:none}</style></head><body>
<div class=side><button onclick="location.reload()" style="width:100%;padding:10px;background:#2f2f2f;color:#fff;border:1px solid #333;border-radius:10px">+ New Chat</button><p style="font-size:11px;opacity:0.4;margin-top:20px">Andhariki AI v3 - Working!</p></div>
<div class=main><div class=top>Andhariki AI - Personal Assistant</div><div class=chat id=chat><div id=messages><div style=text-align:center;margin-top:15%;opacity:0.6><h2>Andhariki AI Ready! 🚀</h2><p>ChatGPT la adugu babooie!</p></div></div></div><div class=area><div class=box><input id=inp placeholder="Message Andhariki AI..." onkeypress="if(event.key==='Enter')send()"><button class=send onclick=send()>↑</button></div></div></div>
<script>let msgs=document.getElementById('messages');let history=[];function addMsg(t){let d=document.createElement('div');d.className='msg';d.textContent=t;msgs.appendChild(d);document.getElementById('chat').scrollTop=99999}async function send(){let inp=document.getElementById('inp');let text=inp.value.trim();if(!text)return;if(msgs.innerHTML.includes('Ready!'))msgs.innerHTML='';addMsg('You: '+text);history.push({role:'user',content:text});inp.value='';let typing=document.createElement('div');typing.textContent='Andhariki AI typing...';msgs.appendChild(typing);let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:history})});let data=await r.json();typing.remove();addMsg('Andhariki AI: '+data.reply);history.push({role:'assistant',content:data.reply});}</script></body></html>"""

@app.route("/")
def home(): return HTML
@app.route("/chat", methods=["POST"])
def chat_api():
    history = request.json.get("history", [])
    return jsonify({"reply": ask_groq(history)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
