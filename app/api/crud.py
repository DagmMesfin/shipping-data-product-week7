from sqlalchemy.sql import text
from .database import SessionLocal

def get_top_detected_products(limit=10):
    query = text("""
        SELECT detected_class, COUNT(*) as count
        FROM raw.fct_image_detections
        GROUP BY detected_class
        ORDER BY count DESC
        LIMIT :limit
    """)
    with SessionLocal() as db:
        return db.execute(query, {"limit": limit}).fetchall()


def get_channel_activity(channel):
    query = text("""
        SELECT DATE(date) as day, COUNT(*) as post_count
        FROM raw.telegram_messages
        WHERE channel = :channel
        GROUP BY DATE(date)
        ORDER BY day
    """)
    with SessionLocal() as db:
        return db.execute(query, {"channel": channel}).fetchall()


def search_messages(query_string):
    query = text("""
        SELECT message_id, channel, date, text
        FROM raw.telegram_messages
        WHERE text ILIKE :pattern
        LIMIT 50
    """)
    with SessionLocal() as db:
        return db.execute(query, {"pattern": f"%{query_string}%"}).fetchall()
