from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Andhariki AI</title>
<style>
body{
  font-family:Arial;
  margin:0;
  min-height:100vh;
  display:flex;
  justify-content:center;
  padding:10px;
  /* NEW BACKGROUND - MANDU DESIGN */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-attachment: fixed;
}
.box{
  background:rgba(255,255,255,0.95);
  width:100%;
  max-width:400px;
  border-radius:20px;
  display:flex;
  flex-direction:column;
  height:85vh;
  box-shadow:0 10px 30px rgba(0,0,0,0.3);
  backdrop-filter: blur(10px);
}
.head{
  padding:15px;
  text-align:center;
  font-weight:bold;
  border-bottom:1px solid #eee;
  background: linear-gradient(90deg, #667eea, #764ba2);
  color:white;
  border-radius:20px 20px 0 0;
  font-size:18px;
}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:8px}
.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px 18px 2px 18px;align-self:flex-end;max-width:80%}
.bot{background:#f0f0f5;padding:10px 14px;border-radius:18px 18px 18px 2px;align-self:flex-start;max-width:85%;white-space:pre-wrap;color:#333}
.foot{display:flex;gap:8px;padding:12px;background:#fff;border-radius:0 0 20px 20px}
input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc;outline:none}
button{padding:12px 18px;border-radius:25px;border:none;background: linear-gradient(90deg, #667eea, #764ba2);color:#fff;font-weight:bold}
</style></head>
<body><div class="box"><div class="head">🤖 Andhariki AI - Satya</div>
<div id="chat"><div class="bot">Hi Satya! Background marchesa! 😍 Yee question adugu - Hi avasaram ledu!</div></div>
<div class="foot"><input id="m" placeholder="Type chey..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div></div>
<script>
async function send(){
 let i=document.getElementById("m");let v=i.value.trim();if(!v)return;
 let c=document.getElementById("chat");c.innerHTML+=`<div class=user>${v}</div>`;i.value="";c.scrollTop=c.scrollHeight;
 let id="a"+Date.now();c.innerHTML+=`<div class=bot id=${id}>Typing... ✍️</div>`;
 try{
  let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:v})});
  let d=await r.json();document.getElementById(id).innerText=d.reply
 }catch(e){document.getElementById(id).innerText="Error:"+e}
 c.scrollTop=c.scrollHeight;
}
</script></body></html>
'''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.get_json().get('message','')
        key = os.environ.get('GEMINI_API_KEY')
        if not key:
            return jsonify({"reply":"API KEY ledu!"})
        from google import genai
        client = genai.Client(api_key=key)
        # KOTTHA MODEL - FIXED
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=msg
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)[:400]}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
