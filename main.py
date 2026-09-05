from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(_name_)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Andhariki AI Chatbot</title>
<style>
body { font-family: Arial; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
.chat-box { background: white; width: 400px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 20px; }
.message { padding: 10px; margin: 10px 0; border-radius: 10px; }
.user { background: #0084ff; color: white; text-align: right; }
.bot { background: #e4e6eb; }
input { width: 75%; padding: 10px; border-radius: 20px; border: 1px solid #ccc; }
button { padding: 10px 15px; border-radius: 20px; border: none; background: #0084ff; color: white; }
</style>
</head>
<body>
<div class="chat-box">
<h2>Andhariki AI Chatbot 🤖</h2>
<div id="chat"></div>
<input id="msg" placeholder="Message type chey...">
<button onclick="send()">Send</button>
</div>
<script>
async function send(){
 let m = document.getElementById('msg').value;
 if(!m) return;
 document.getElementById('chat').innerHTML += <div class='message user'>${m}</div>;
 document.getElementById('msg').value='';
 let res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:m})});
 let data = await res.json();
 document.getElementById('chat').innerHTML += <div class='message bot'>${data.reply}</div>;
}
</script>
</body>
</html>
