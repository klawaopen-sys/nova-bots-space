# Google Sheets Templates / Шаблоны Google Таблиц / Шаблони Google Таблиць

This directory contains database templates for the Zapisukha booking bot in CSV format. You can import these directly into your Google Sheets.

В этой директории находятся шаблоны таблиц для базы данных бота «Записуха» в формате CSV. Вы можете импортировать их напрямую в Google Таблицы.

У цій директорії знаходяться шаблони таблиць для бази даних бота «Записуха» у форматі CSV. Ви можете імпортувати їх безпосередньо в Google Таблиці.

---

## How to Import / Как импортировать / Як імпортувати:

1. Create a new Google Sheet.
2. Choose your language (English, Russian, or Ukrainian).
3. Import each CSV file into a separate sheet (tab) inside your Google Sheet:
   * Go to **File** -> **Import** -> **Upload**.
   * Upload the CSV file.
   * Select **Replace current sheet** or **Insert new sheet**.
4. Rename each sheet (tab) in Google Sheets to match the filename (without the prefix):
   * **Ukrainian:** `Клієнти`, `Записи`, `Вихідні`, `БлокЧас`, `Прайс`
   * **Russian:** `Клиенты`, `Записи`, `Выходные`, `БлокВремя`, `Прайс`
   * **English:** `Clients`, `Appointments`, `Holidays`, `BlockedTime`, `Prices`
5. Configure `DEFAULT_LANG` in your `.env` to match the selected language (`uk`, `ru`, or `en`). The bot will automatically map sheet names and column headers!

---

## File Mapping / Соответствие файлов / Відповідність файлів:

| Sheet Purpose | Ukrainian (uk) | Russian (ru) | English (en) |
| :--- | :--- | :--- | :--- |
| **Clients** | `uk_clients.csv` | `ru_clients.csv` | `en_clients.csv` |
| **Appointments** | `uk_appointments.csv` | `ru_appointments.csv` | `en_appointments.csv` |
| **Holidays** | `uk_holidays.csv` | `ru_holidays.csv` | `en_holidays.csv` |
| **Blocked Time** | `uk_blocked_time.csv` | `ru_blocked_time.csv` | `en_blocked_time.csv` |
| **Prices** | `uk_price.csv` | `ru_price.csv` | `en_price.csv` |
