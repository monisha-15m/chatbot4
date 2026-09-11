# Gemini Flask Chatbot

A minimal AI chatbot built with **Flask** + **Google Gemini API** (`gemini-3.6-flash`),
ready to push to **GitHub** and deploy on **Render**.

## Project structure

```
gemini-flask-chatbot/
├── app.py                # Flask backend + Gemini API calls
├── templates/
│   └── index.html        # Chat UI
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── Procfile               # tells Render/Heroku how to start the app
├── render.yaml             # Render "Blueprint" (optional one-click config)
├── .env.example
└── .gitignore
```

## 1. Run locally

```bash
# 1. Clone / unzip, then enter the folder
cd gemini-flask-chatbot

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# edit .env and paste your key:
# GEMINI_API_KEY=xxxxxxxxxxxxxxxx

# 5. Run
python app.py
```

Open http://localhost:5000 in your browser.

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

## 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Gemini Flask chatbot"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

`.env` is already in `.gitignore` — never commit your real API key.

## 3. Deploy on Render

**Option A — Dashboard (recommended for first time)**
1. Go to https://dashboard.render.com → **New** → **Web Service**.
2. Connect your GitHub repo.
3. Render should auto-detect Python. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Under **Environment**, add:
   - `GEMINI_API_KEY` = your key
   - `GEMINI_MODEL` = `gemini-3.6-flash`
5. Click **Create Web Service**. Render builds and deploys automatically on every push.

**Option B — Blueprint (`render.yaml`)**
1. In Render, choose **New** → **Blueprint**, point it at this repo.
2. Render reads `render.yaml` and creates the service for you.
3. You'll be prompted to enter the `GEMINI_API_KEY` value (it's marked `sync: false` so it's never stored in the repo).

Once deployed, Render gives you a live URL like:
`https://gemini-flask-chatbot.onrender.com`

## Notes

- Chat history is kept **in memory per session id**, which resets whenever the
  server restarts (normal on Render's free tier when it spins down after inactivity).
  For persistent history, swap the `sessions` dict in `app.py` for Redis or a database.
- Swap `GEMINI_MODEL` in your environment variables to use a different Gemini
  model (e.g. `gemini-3.1-flash-lite` for a cheaper/faster option) without touching code.
- `/healthz` is available for uptime checks.
