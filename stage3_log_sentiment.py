# stage3_log_sentiment.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3, datetime

analyzer = SentimentIntensityAnalyzer()

def analyze(text):
    s = analyzer.polarity_scores(text)
    return "positive" if s["compound"] > 0.05 else "negative" if s["compound"] < -0.05 else "neutral"

def log_to_db(text, sentiment, pose="unknown"):
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        pose TEXT,
        text TEXT,
        sentiment TEXT
    )''')
    cursor.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, ?)", (
        None, datetime.datetime.now().isoformat(), pose, text, sentiment
    ))
    conn.commit()
    conn.close()
