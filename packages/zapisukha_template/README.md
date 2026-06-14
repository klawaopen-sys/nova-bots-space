# White-Label Telegram Beauty Salon Booking Bot Template ("Zapisukha")

A premium, production-ready, and fully automated Telegram scheduling bot designed for beauty salons, nail masters, cosmetologists, and independent specialists. It features dynamic multi-language (i18n) support, a 2/2 custom work schedule (switching between salon and home shifts), slot booking validation, auto-discount promotions, and direct integration with Google Sheets as its primary database (meaning zero state loss on redeployment!).

## Key Features

1. **Google Sheets Integration:** No complex SQL setups required. All appointments, client details, work schedules, block-times, and price lists are stored directly in your Google Sheets spreadsheet.
2. **Dynamic Multilinguality (i18n):** Automatically reads the user's Telegram interface language (English, Ukrainian, Russian, etc.) and serves all replies and buttons in that language.
3. **Smart Shift Calendar:** Supports split addresses (e.g. Salon vs Home shifts) automatically determined using a rolling 2/2 schedule from a defined start date.
4. **FSM Booking Engine:** Guide clients step-by-step through selecting a date, picking available timeslots, selecting a service, writing custom wishes, and confirming details.
5. **Admin Dashboard:** Access today's and tomorrow's lists of appointments, block custom days/hours, and manage schedules directly through inline admin controls inside Telegram.
6. **Automatic Promos:** Detects returning customers and triggers a custom discount (e.g., 10% off) if they haven't booked a visit in over 21 days.

---

## Google Sheets API Setup Guide

Since this bot uses Google Sheets to store database rows, you must create a Service Account and share your Google Sheet with it.

### 1. Create a Google Service Account
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `zapisukha-booking-bot`).
3. Navigate to **APIs & Services** -> **Library**. Search for **Google Sheets API** and **Google Drive API** and click **Enable** for both.
4. Go to **APIs & Services** -> **Credentials**. Click **+ Create Credentials** -> **Service Account**.
5. Fill in the details, click **Create and Continue**, and select the **Editor** role. Click **Done**.
6. Find your new Service Account in the list, click the **Keys** tab -> **Add Key** -> **Create New Key**.
7. Select **JSON** format and click **Create**. This will download a `.json` key file.
8. Rename this downloaded file to `credentials.json` and move it into the root directory of this bot.

### 2. Share Your Google Sheet
1. Create a new Google Sheet in your Google Drive.
2. Open the Sheet and click the **Share** button.
3. Paste the Service Account email address (found in your `credentials.json` file as `client_email`) and give it **Editor** permissions.
4. Copy the unique **Google Sheets ID** from the URL of your spreadsheet:
   `https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEETS_ID/edit`
5. Save this ID to your `.env` file as `GOOGLE_SHEETS_ID`.

### 3. Setup Sheet Structure
Create worksheets in your Google Sheet with the following names:
* **Клієнти** (Columns: `ID`, `Ім'я`, `Телефон`, `Username`, `Нотатки`, `Дата`, `Статус`, `Крок`, `Фото`, `MsgID`)
* **Записи** (Columns: `ID`, `Дата`, `Час`, `КлієнтID`, `Послуга`, `Статус`, `Побажання`, `Ціна`)
* **Вихідні** (Single column: `Дата`)
* **БлокЧас** (Columns: `Дата`, `Час`)
* **Прайс** (Columns: `Послуга`, `Ціна` - e.g. Row 1: `💅 Манікюр` | `580`)

---

## Installation & Local Setup

### 1. Telegram Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram and run `/newbot`.
2. Save your `BOT_TOKEN`.
3. In `/admin` settings of BotFather, you can set your commands:
   - `start` - main menu
   - `admin` - admin dashboard

### 2. Environment Variables (.env)
Create a `.env` file in the root directory (copy `.env.example`) and fill in:
```ini
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_IDS=YOUR_TELEGRAM_USER_ID

GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_ID=YOUR_GOOGLE_SHEETS_ID

# Customized locations
ADDRESS_SALON=📍 Main St. 128 (Salon)
ADDRESS_HOME=🏠 Sunshine Ave. 15 (Home)

SHIFT_START_DATE=2026-04-21
WORK_HOURS=10:00,12:00,14:00,16:00
```

### 3. Run Locally
1. Activate virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

---

## Git & GitHub Setup (Crucial for Deployment)

To deploy your bot to hosting platforms like Railway, you must push your local code to a Git repository.

> [!WARNING]
> **Always make sure your GitHub repository is PRIVATE.** Setting it to public will expose your `.env` configuration, secret Google credentials file, and bot tokens to the public!

1. **Initialize Git locally:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for booking bot template"
   ```
2. **Create a Private GitHub Repo:**
   - Go to [GitHub](https://github.com/) and create a new repository.
   - Set the visibility strictly to **Private**.
   - Do **NOT** initialize it with any files.
3. **Link and Push:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git branch -M main
   git push -u origin main
   ```

---

## Deployment (Railway)

This template includes a **Procfile** and is fully ready for zero-configuration deployment on Railway:
1. Sign in on [Railway](https://railway.app/).
2. Create a **New Project** -> **Deploy from GitHub repository**.
3. Select your **Private** repository.
4. In the **Variables** tab of the Railway dashboard, add all environment variable keys from your `.env` file.
5. In addition, you must paste the contents of your `credentials.json` directly. You can specify a variable `GOOGLE_CREDENTIALS_CONTENT` and configure your `config.py` to read credentials directly from it, or push `credentials.json` safely (since the repo is **Private**, but standard practice is pasting content into a Railway variable to avoid committing key files).
   > [!TIP]
   > Since the repository is Private, you can commit `credentials.json` safely, but for maximum safety, you can add it to `.gitignore` and specify configuration keys directly in your cloud environment.

Railway will build and run the bot immediately. Since all appointments are stored in Google Sheets, restarting container instances will not result in any data loss!

---

## License & Support
Distributed under the MIT License. For custom integrations, contact our support team.
