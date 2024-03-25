from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from logging_service import LoggingService

app = FastAPI()
logging_service = LoggingService()


class LogItem(BaseModel):
    uuid: str
    message: str


@app.post("/log/")
async def log_message(log_item: LogItem):
    return logging_service.log_message(log_item.uuid, log_item.message)


@app.get("/messages/")
async def get_messages():
    return logging_service.get_messages()
