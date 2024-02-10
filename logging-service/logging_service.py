from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
logged_messages = {}


class LogItem(BaseModel):
    uuid: str
    message: str


@app.post("/log/")
async def log_message(log_item: LogItem):
    logged_messages[log_item.uuid] = log_item.message
    return {"status": "logged"}


@app.get("/messages/")
async def get_messages():
    return " ".join(logged_messages.values())
