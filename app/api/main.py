from fastapi import FastAPI, Query
from . import crud

app = FastAPI(
    title="Telegram Insight API",
    description="API for Telegram channel insights and product detection. Access interactive Swagger UI at /docs.",
    version="1.0",
)

@app.get("/reports/top-products")
def top_products(limit: int = 10):
    return [
        {"class": row[0], "count": row[1]}
        for row in crud.get_top_detected_products(limit)
    ]


@app.get("/channels/{channel_name}/activity")
def channel_activity(channel_name: str):
    return [
        {"date": str(row[0]), "post_count": row[1]}
        for row in crud.get_channel_activity(channel_name)
    ]


@app.get("/search/messages")
def search(query: str = Query(..., min_length=2)):
    return [
        {"message_id": row[0], "channel": row[1], "date": str(row[2]), "text": row[3]}
        for row in crud.search_messages(query)
    ]
