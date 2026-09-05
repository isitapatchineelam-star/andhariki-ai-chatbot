from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(_name_)

# Try to load Gemini only if key exists
try:
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        HAS_GEMINI = True
    else:
        HAS_GEMINI = False
except:
    HAS_GEMINI = False

HTML_PAGE = """
<!DOCTYPE html>
<html><head><title>Andhariki AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;padding:20px}
.chat-box{background:white;width:400px;max-width:95%;border-radius:15px;padding:20px;box-shadow:0 4px 15px rgba(0,0,0,0.1)}
.header{background:#0084ff;color:white;padding:15px;border-radius:10px;text-align:center;margin-bottom:15px}
.message{padding:10px 15px;margin:10px 0;border-radius:18px;max-width:80%}
.user{background:#0084ff;color:white;margin-left:auto;text-align:right}
.bot{background:#e4e6eb;color:black}
.input-area{display:flex;gap:10px;margin-top:15px}
input{flex:1;padding:12px;border-radius:25px;border:1px solid #ccc;outline:none}
button{padding:12px 20px;border-radius:25px;border:none;background:#0084ff;color:white;cursor:pointer}
</style>
</head><body>
<div class="chat-box">
<div class="header"><h3 style="margin:0">Andhariki AI Chatbot 🤖</h3><small>by Satya</small></div>
<div id="chat"><div class='message bot'>Hi! Nenu Andhariki AI ni! Em help kavali? 🙏</div></div>
<div class="input-area"><input id="msg" placeholder="Message..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div>
</div>
<script>
async function send(){
 let m=document.getElementById('msg').value.trim();if(!m)return;
 document.getElementById('chat').innerHTML+=<div class='message user'>${m}</div>;
 document.getElementById('msg').value='';
 document.getElementById('chat').scrollTop=99999;
 try{
  let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
  let data=await res.json();
  document.getElementById('chat').innerHTML+=<div class='message bot'>${data.reply}</div>;
 }catch(e){document.getElementById('chat').innerHTML+=<div class='message bot'>Error - malli try chey!</div>;}
}
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message','')
    if not user_msg:
        return jsonify({"reply":"Message pampu Satya!"})
    
    # If Gemini key is there, use AI
    if HAS_GEMINI:
        try:
            response = model.generate_content(user_msg)
            return jsonify({"reply": response.text})
        except Exception as e:
            pass
    
    # Fallback without key - Simple replies
    low = user_msg.lower()
    if 'hi' in low or 'hello' in low:
        reply = "Hi Satya! 🙏 Nenu Andhariki AI! Gemini key lekunna kuda nenu work avutunna! Key add cheste inka smart avta!"
    elif 'ela unnav' in low:
        reply = "Nenu super ga unna! Nee chatbot ippudu LIVE lo undi! 🎉"
    elif 'peru' in low:
        reply = "Naa peru Andhariki AI - Satya create chesadu!"
    elif 'thank' in low:
        reply = "Welcome Satya! 😊"
    else:
        reply = f"Nuvvu '{user_msg}' annav! Ippudu nenu simple mode lo unna. Render lo GEMINI_API_KEY add cheste full AI la work avta! Kani ippatiki LIVE ayya ga!"

    return jsonify({"reply": reply})

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
