from flask import Flask, request, jsonify
import os

app = Flask(_name_)

@app.route('/')
def home():
    return """
    <html>
    <head><title>Andhariki AI</title></head>
    <body style="font-family:Arial;text-align:center;padding:30px;background:#f0f2f5">
    <div style="background:white;padding:20px;border-radius:15px;max-width:400px;margin:auto">
    <h2>Andhariki AI 🤖</h2>
    <p>Hi Satya! Nenu LIVE ayyanu!</p>
    <input id="m" placeholder="Hi type chey" style="padding:10px;width:70%;border-radius:20px;border:1px solid #ccc">
    <button onclick="send()" style="padding:10px 15px;border-radius:20px;background:#0084ff;color:white;border:none">Send</button>
    <div id="chat" style="margin-top:20px;text-align:left"></div>
    </div>
    <script>
    async function send(){
      let v=document.getElementById('m').value;
      if(!v)return;
      document.getElementById('chat').innerHTML+='<p><b>You:</b> '+v+'</p>';
      document.getElementById('m').value='';
      let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});
      let d=await r.json();
      document.getElementById('chat').innerHTML+='<p><b>Bot:</b> '+d.reply+'</p>';
    }
    </script>
    </body></html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    m = request.json.get('message','').lower()
    if 'hi' in m:
        reply = "Hi Satya! 🙏 Andhariki AI LIVE lo undi! 🎉"
    else:
        reply = f"Nuvvu '{m}' annav! Nenu work avutunna!"
    return jsonify({"reply": reply})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
