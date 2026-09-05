from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Andhariki AI</title><style>body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;padding:15px;margin:0}.box{background:#fff;width:100%;max-width:400px;border-radius:20px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,.1)}#chat{height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:8px;margin:12px 0}.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px;align-self:flex-end;max-width:80%}.bot{background:#e4e6eb;color:#000;padding:10px 14px;border-radius:18px;align-self:flex-start;max-width:80%}input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc;outline:none}button{padding:12px 18px;border-radius:25px;border:none;background:#0084ff;color:#fff;font-weight:bold}.row{display:flex;gap:8px}</style></head><body><div class="box"><h3 style="text-align:center">Andhariki AI 🤖</h3><div id="chat"><div class="bot">Hi Satya! Nenu ready! Em adagali? 😊</div></div><div class="row"><input id="m" placeholder="Type chey..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div></div><script>async function send(){let i=document.getElementById('m');let v=i.value.trim();if(!v)return;let c=document.getElementById('chat');c.innerHTML+=`<div class=user>${v}</div>`;i.value='';c.scrollTop=c.scrollHeight;let id='t'+Date.now();c.innerHTML+=`<div class=bot id=${id}>Typing...</div>`;c.scrollTop=c.scrollHeight;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let txt=await r.text();let d;try{d=JSON.parse(txt)}catch(e){d={reply:"Server error: "+txt.slice(0,200)}}document.getElementById(id).innerText=d.reply}catch(e){document.getElementById(id).innerText="Error: "+e.message}c.scrollTop=c.scrollHeight}</script></body></html>"""

@app.route('/chat', methods=['POST'])
def chat():
    # Eppudu JSON ne return chestam - HTML vaddu!
    try:
        data = request.get_json(force=True, silent=True) or {}
        msg = data.get('message','').strip()
        if not msg:
            return jsonify({"reply": "Message ledu Satya!"})

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key or len(api_key) < 20:
            return jsonify({"reply": "⚠️ GEMINI_API_KEY ledu! Render -> Environment lo key pettu. Key 'AIza...' tho start avvali!"})

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(msg)
            if hasattr(res, 'text') and res.text:
                return jsonify({"reply": res.text})
            else:
                return jsonify({"reply": "Gemini empty reply ichindi - malli try chey!"})
        except ImportError as e:
            return jsonify({"reply": f"Library ledu: {e}. requirements.txt lo google-generativeai unda chudu!"})
        except Exception as e:
            err = str(e)
            if "API_KEY" in err or "400" in err:
                return jsonify({"reply": f"API Key thappu! Key check chey: {err[:150]}"})
            if "quota" in err.lower() or "429" in err:
                return jsonify({"reply": "Gemini quota ayipoyindi! 1 min aagi try chey, leka kotta key teesuko aistudio.google.com nundi!"})
            return jsonify({"reply": f"Gemini Error: {err[:200]}"})

    except Exception as e:
        # Last safety net - eppudu JSON!
        return jsonify({"reply": f"Server Error: {str(e)[:200]}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
