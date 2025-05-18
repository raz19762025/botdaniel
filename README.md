# Integrated FastAPI + Telegram Bot

## Setup

1. Copy `.env.example` → `.env` and fill in your credentials.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python run_app.py
   ```

This starts both the Telegram polling bot and FastAPI UI in one process.

## דוחות היסטוריית ערכים

הוספת פקודות בוט חדשות ליצירת דוחות יומיים, שבועיים וחודשיים:
- `/report daily`
- `/report weekly`
- `/report monthly`

המידע נשמר ב-`data/value_history.json` וכולל שינויים יומיים בערך הפורטפוליו.

## התקנת דרישות נוספות
כדי להפעיל את ה-AI pipeline, חשוב להתקין את הספרייה `ta`:
```
pip install ta
```
