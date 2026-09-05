from flask import Flask, request, jsonify
import os

app = Flask(_name_)

# Gemini ni try chestam, error vachina app crash avvoddu
try:
    import google.generativeai as genai
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        genai.configure(api_key=key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        gemini_model = None
except Exception as e:
    print(f"Gemini error: {e}")
    gemini_model = None

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Andhariki AI</title>
<style>
body{font-family:Arial;background:#f0f2f5;margin:0;padding:15px;display:flex;justify-content:center}
.box{background:#fff;width:100%;max-width:420px;border-radius:20px;padding:18px;box-shadow:0 4px 15px rgba(0,0,0,0.1)}
#chat{height:60vh;overflow-y:auto;display:flex;flex-direction:column;gap:8px;margin:12px 0}
.user{background:#0084ff;color:#fff;padding:10px 14px;border-radius:18px 18px 4px 18px;align-self:flex-end;max-width:80%}
.bot{background:#e4e6eb;color:#000;padding:10px 14px;border-radius:18px 18px 18px 4px;align-self:flex-start;max-width:80%}
.input{display:flex;gap:8px;margin-top:10px}
input{flex:1;padding:12px 16px;border-radius:25px;border:1px solid #ccc;outline:none}
button{padding:12px 18px;border-radius:25px;border:none;background:#0084ff;color:#fff;font-weight:bold;cursor:pointer}
</style></head><body>
<div class="box">
<h2 style="text-align:center;margin:0">Andhariki AI 🤖</h2>
<p style="text-align:center;color:#888;font-size:13px;margin:5px 0 15px 0">Adugu - Telugu, English, Hindi lo chepta!</p>
<div id="chat"><div class="bot">Hi Satya! Nenu Andhariki AI ni 😊 Naku emaina adugu!</div></div>
<div class="input">
<input id="msg" placeholder="Type chey..." onkeypress="if(event.key=='Enter')send()">
<button onclick="send()">Send</button>
</div>
</div>
<script>
async function send(){
 let i=document.getElementById('msg'); let text=i.value.trim(); if(!text) return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=<div class='user'>${text}</div>; i.value=''; chat.scrollTop=chat.scrollHeight;
 let id='b'+Date.now(); chat.innerHTML+=<div class='bot' id='${id}'>Thinking...</div>; chat.scrollTop=chat.scrollHeight;
 try{
   let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
   let data=await res.json();
   document.getElementById(id).innerText=data.reply;
 }catch(e){
   document.getElementById(id).innerText='Error vachindi: '+e.message;
 }
 chat.scrollTop=chat.scrollHeight;
}
</script></body></html>
    """

@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        user_msg = request.json.get('message','')
        if not gemini_model:
            return jsonify({"reply": "⚠️ GEMINI_API_KEY set cheyaledu! Render -> Environment lo key add chey Satya."})
        
        # Gemini ki pampadam
        response = gemini_model.generate_content(f"You are Andhariki AI, helpful friendly chatbot. Answer in same language as user (Telugu/English/Hindi). User: {user_msg}")
        reply_text = response.text
        return jsonify({"reply": reply_text})
        
    except Exception as e:
        error_str = str(e)
        print(f"ERROR: {error_str}")
        if "quota" in error_str.lower() or "429" in error_str:
            return jsonify({"reply": "Gemini busy ayindi (quota). 1 min tarvata try chey Satya! 🙏"})
        return jsonify({"reply": f"Error: {error_str[:200]}"})

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
