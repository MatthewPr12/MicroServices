from fastapi import FastAPI
from message_service import message_service, logger

app = FastAPI()


@app.on_event("shutdown")
def shutdown_event():
    message_service.stop_consuming()


@app.get("/messages/")
async def get_messages():
    logger.info("Received request for messages.")
    try:
        messages = message_service.get_messages()
        return {"messages": messages}
    except Exception as exc:
        logger.exception("Failed to get messages: ", exc)
        return {"error": "Failed to get messages"}
