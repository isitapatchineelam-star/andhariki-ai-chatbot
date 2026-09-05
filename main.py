from flask import Flask, request, jsonify, render_template_string
import os
app = Flask(_name_)
HTML_PAGE = """<html><head><title>Andhariki AI</title><style>body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;padding:20px}.chat-box{background:white;width:380px;border-radius:15px;padding:20px;box-shadow:0 4px 10px rgba(0,0,0,.1)}.msg{padding:10px;margin:8px 0;border-radius:10px}.user{background:#0084ff;color:white;text-align:right}.bot{background:#e4e6eb}input{width:70%;padding:10px;border-radius:20px;border:1px solid #ccc}button{padding:10px 15px;border-radius:20px;border:none;background:#0084ff;color:white}</style></head><body><div class="chat-box"><h2>Andhariki AI 🤖</h2><div id="chat"><div class='msg bot'>Hi Satya! Nenu LIVE ayyanu! 😊</div></div><input id="m" placeholder="Hi ani type chey"><button onclick="send()">Send</button></div><script>async function send(){let v=document.getElementById('m').value;if(!v)return;document.getElementById('chat').innerHTML+=<div class='msg user'>${v}</div>;document.getElementById('m').value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:v})});let d=await r.json();document.getElementById('chat').innerHTML+=<div class='msg bot'>${d.reply}</div>;}</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML_PAGE)
@app.route('/chat',methods=['POST'])
def chat():
 m=request.json.get('message','').lower()
 if 'hi' in m: reply="Hi Satya! 🙏 Andhariki AI LIVE lo undi! 🎉"
 else: reply=f"Nuvvu '{m}' annav! Nenu work avutunna!"
 return jsonify({"reply":reply})
if _name=='main_': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
