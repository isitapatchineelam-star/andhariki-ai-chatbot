from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
GROQ_KEY = os.environ.get("GROQ_API_KEY", "").strip()

def ask_groq(history):
    if not GROQ_KEY:
        return "⚠️ Render lo GROQ_API_KEY ledu babooie! Groq.com nundi key techi Environment lo pettu."

    try:
        msgs = [{"role":"system","content":"You are Andhariki AI - Personal Assistant like ChatGPT. Friendly Telugu+English mix, call user babooie. Give real helpful answers."}]
        for h in history[-8:]:
            msgs.append(h)

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
            json={"model":"llama-3.1-8b-instant","messages":msgs,"temperature":0.7},
            timeout=30)

        data = r.json()
        print("GROQ RESPONSE:", data) # Render Logs lo kanipistadi

        if "choices" not in data:
            err = data.get("error", {}).get("message", str(data))
            return f"Groq API Error babooie: {err} - Key thappu ayite kotta key pettu!"

        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

HTML = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>Andhariki AI - Personal Assistant</title>
<style>*{box-sizing:border-box}body{margin:0;background:#212121;color:#ececec;font-family:sans-serif;display:flex;height:100vh}.side{width:260px;background:#171717;padding:12px;display:flex;flex-direction:column}.main{flex:1;display:flex;flex-direction:column}.top{padding:12px;text-align:center;border-bottom:1px solid #333;font-weight:600}.chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;margin:0 auto;width:100%}.msg{margin:16px 0;white-space:pre-wrap;line-height:1.6}.area{padding:16px}.box{max-width:800px;margin:0 auto;background:#2f2f2f;border-radius:28px;display:flex;padding:10px 14px;gap:8px}.box input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:16px}.send{background:#fff;color:#000;width:32px;height:32px;border-radius:50%;border:none}</style></head><body>
<div class=side><button onclick="location.reload()" style="width:100%;padding:10px;background:#2f2f2f;color:#fff;border:1px solid #333;border-radius:10px">+ New Chat</button><p style="font-size:12px;opacity:0.5;margin-top:20px">Andhariki AI v2.0 - ChatGPT Clone</p></div>
<div class=main><div class=top>Andhariki AI - Personal Assistant</div><div class=chat id=chat><div id=messages><div style=text-align:center;margin-top:15%;opacity:0.6><h2>Andhariki AI Ready! 🚀</h2><p>Ye question aina adugu babooie!</p></div></div></div><div class=area><div class=box><input id=inp placeholder="Message Andhariki AI..." onkeypress="if(event.key==='Enter')send()"><button class=send onclick=send()>↑</button></div></div></div>
<script>
let msgs=document.getElementById('messages'), inp=document.getElementById('inp');
function addMsg(t){let d=document.createElement('div');d.className='msg';d.textContent=t;msgs.appendChild(d);document.getElementById('chat').scrollTop=99999}
async function send(){let text=inp.value.trim();if(!text)return;if(msgs.innerHTML.includes('Ready!'))msgs.innerHTML='';addMsg('You: '+text);inp.value='';let typing=document.createElement('div');typing.textContent='Andhariki AI typing...';msgs.appendChild(typing);let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({history:[{role:'user',content:text}]})});let data=await r.json();typing.remove();addMsg('Andhariki AI: '+data.reply);}
</script></body></html>"""

@app.route("/")
def home(): return HTML

@app.route("/chat", methods=["POST"])
def chat_api():
    history = request.json.get("history", [])
    ans = ask_groq(history)
    return jsonify({"reply": ans})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
