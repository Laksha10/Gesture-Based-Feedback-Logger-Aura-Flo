# feedback_logger.py
import sqlite3
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Initialize DB (if not exists)
def init_db(db_path="feedback_logs.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            text TEXT,
            distance REAL,
            sentiment TEXT
        )
    """)
    conn.commit()
    conn.close()


# Save new entry
def save_feedback(text, distance, db_path="feedback_logs.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sentiment = classify_sentiment(text)
    cursor.execute(
        "INSERT INTO feedback (timestamp, text, distance, sentiment) VALUES (?, ?, ?, ?)",
        (timestamp, text, distance, sentiment)
    )
    conn.commit()
    conn.close()
    print(f"🗄️ Logged feedback at {timestamp} — Sentiment: {sentiment}")


def classify_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.5:
        return 'positive'
    elif compound <= -0.5:
        return 'negative'
    elif 'pain' in text.lower() or 'ache' in text.lower():
        return 'pain-related'
    else:
        return 'neutral'