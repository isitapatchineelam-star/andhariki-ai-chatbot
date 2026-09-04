# Andhariki

Public Flask AI chatbot powered by Google Gemini. The API key stays on the server and is read from the `GEMINI_API_KEY` environment variable.

## Run locally

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python main.py
```

Then open `http://localhost:5000`.

For deployment, use:

```bash
gunicorn main:app
```

Set `GEMINI_API_KEY` as a Secret in the deployment environment. Never put the key in frontend JavaScript or commit it to a file.