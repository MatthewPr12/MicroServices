from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(thread)d] - %(name)s - %(levelname)s - %(message)s",
    filename="logging_service.log"
)
logger = logging.getLogger("logging_service")

app = FastAPI()
logged_messages = {}


class LogItem(BaseModel):
    uuid: str
    message: str


@app.post("/log/")
async def log_message(log_item: LogItem):
    logger.info(f"Logging message: {log_item.message} with UUID: {log_item.uuid}")
    logged_messages[log_item.uuid] = log_item.message
    return {"status": "logged"}


@app.get("/messages/")
async def get_messages():
    logger.info("Returning all logged messages.")
    return " ".join(logged_messages.values())
