from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Andhariki AI LIVE ayindi Satya! 🎉</h1><p>Nee chatbot ready!</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
