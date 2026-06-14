# White-Label Telegram Marketplace Bot Template (Multi-City Classifieds Hub)

A production-ready, highly scalable, and fully automated Telegram classifieds marketplace bot. It supports ИИ-moderation via Gemini, Whisper voice dictation via Groq, dynamic multi-language (i18n) detection, user limits, multi-level referrals, and Telegram Stars VIP bumps.

## Key Features

1. **Multi-City Configuration (White-Label):** Launch a local marketplace for *any* city (Kyiv, Berlin, New York, Warsaw, London) simply by changing the `CITY_NAME` variable in the `.env` file. The bot dynamically adapts all database files, command replies, welcome menus, and banners to the specified city.
2. **Dynamic Multilinguality (i18n):** The bot automatically detects the user's Telegram interface language (English, Ukrainian, Russian, etc.) and serves all replies and buttons in that language.
3. **ИИ-Moderation (Google Gemini):** Automatically filters uploaded listing images using the `gemini-2.5-flash` model. If a user uploads irrelevant images (e.g., memes, garbage, or inappropriate content), the bot automatically rejects the listing during FSM registration.
4. **Voice Dictation (Groq Whisper):** Users can dictate listing titles, descriptions, and prices by sending voice messages. The bot transcribes the audio using Groq's `whisper-large-v3-turbo` with high accuracy and fills out the text fields.
5. **Subscription & Stars Integration:** Includes a weekly/monthly posting limit structure. Users can purchase unlimited posting passes via Telegram Stars (XTR).
6. **Multi-Level Referrals:** Incentivizes organic growth by awarding bonus listing limits to users when their invited friends publish their first listing (rewards levels: Level 1 = +3, Level 2 = +2, Level 3 = +1).
7. **Clean Database Schema:** Runs on SQLite via `aiosqlite` with auto-seeded sections for Cars/Transport, Goods, and Local Services.

---

## Installation & Setup Guide

### 1. Telegram Bot Token Setup
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send the command `/newbot` and follow the instructions to name your bot and get the `BOT_TOKEN`.
3. Save the token to your `.env` file.

### 2. Get API Keys
- **Google Gemini API Key:** Create a key on the [Google AI Studio Console](https://aistudio.google.com/). This is required for ИИ image moderation.
- **Groq API Key:** Sign up at [Groq Console](https://console.groq.com/) and generate an API key. This is required for speech-to-text voice dictation.

### 3. Environment Variables Configuration
Create a `.env` file in the root of the project (copy `.env.example`) and fill in your settings:

```ini
# Bot Token from BotFather
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

# Your numeric Telegram user ID (so you get Admin privileges in the bot)
ADMIN_ID=YOUR_TELEGRAM_USER_ID

# White-Label Customization
CITY_NAME=Berlin   # Name of the target city
DEFAULT_LANG=en    # Default language fallback (en, uk, or ru)

# API Keys
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=whisper-large-v3-turbo

# Optional Proxy
USE_PROXY=False
```

### 4. Local Run (Development)
1. Install Python 3.10 or higher.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows (cmd):
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the bot:
   ```bash
   python main.py
   ```

### 5. Git & GitHub Setup (Crucial for Deployment)
Before deploying the bot to cloud services (like Railway), you need to push your code to a Git repository.

> [!WARNING]
> **Always create a PRIVATE GitHub repository.** Making the repository public will expose your `.env` configuration file, Bot tokens, and private API keys to the world. The included `.gitignore` file will prevent `.env` and SQLite `.db` files from being committed, but extra caution is highly advised.

1. **Initialize a local Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for white-label bot"
   ```
2. **Create a Private GitHub Repository:**
   - Go to [GitHub](https://github.com/) and create a new repository.
   - Set the visibility option to **Private**.
   - Do **NOT** initialize the repository with a README, `.gitignore`, or license, as these are already provided in the template.
3. **Link and Push your local code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   git branch -M main
   git push -u origin main
   ```

### 6. Deployment (Railway / VPS)
This template is fully configured for continuous integration and deployment.

- **Railway Deployment:**
  1. Create an account and log in on [Railway](https://railway.app/).
  2. Click **New Project** -> **Deploy from GitHub repo**.
  3. Select your newly created **Private** repository.
  4. Go to the **Variables** tab in your Railway service dashboard and add all variables from your local `.env` file (e.g. `BOT_TOKEN`, `ADMIN_ID`, `CITY_NAME`, `GEMINI_API_KEY`, `GROQ_API_KEY`, etc.).
  5. Railway will automatically build the environment using the provided `requirements.txt` and start the bot using the command defined in the `Procfile`.
- **Database Persistence (Railway):**
  - By default, Railway's file system is ephemeral (resets on new deployments). To prevent your database from resetting:
    1. In Railway, click **+ New** -> **Volume**.
    2. Mount the volume to a path, for example `/data`.
    3. Add a new variable `DB_NAME` in the **Variables** tab and set it to `/data/ads.db` (or whatever name you prefer), so that the SQLite database is written directly to the persistent volume.

---

## License & Support
Distributed under the MIT License. For custom integrations, white-label setup, or server deployments, contact our support team.
