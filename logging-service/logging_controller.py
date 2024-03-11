from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from logging_service import LoggingService

app = FastAPI()
logging_service = LoggingService()


class LogItem(BaseModel):
    uuid: str
    message: str


# @app.on_event("startup")
# async def startup_event():
#     # This will automatically start the Hazelcast instance when the FastAPI app starts
#     global logging_service
#     logging_service = LoggingService()
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     # This will shut down the Hazelcast instance gracefully when the FastAPI app stops
#     global logging_service
#     logging_service.shutdown()


@app.post("/log/")
async def log_message(log_item: LogItem):
    return logging_service.log_message(log_item.uuid, log_item.message)


@app.get("/messages/")
async def get_messages():
    return logging_service.get_messages()
