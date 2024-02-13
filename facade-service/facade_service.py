from fastapi import FastAPI, HTTPException, Body
from uuid import uuid4
import httpx
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="facade_service.log"
)
logger = logging.getLogger("facade_service")

app = FastAPI()

LOGGING_SERVICE_URL = "http://localhost:8001"
MESSAGES_SERVICE_URL = "http://localhost:8002"


@app.post("/post_message/")
async def post_message(msg: str = Body(...)):
    msg_uuid = str(uuid4())
    logger.info(f"Received message to log: {msg}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{LOGGING_SERVICE_URL}/log/", json={'uuid': msg_uuid, 'message': msg})
        response.raise_for_status()
    except httpx.RequestError as exc:
        logger.error(f"Logging service request failed: {str(exc)}")
        return {"error": str(exc)}

    # return {"uuid": msg_uuid, "response": response.text}
    return response.text


@app.get("/get_messages/")
async def get_messages():
    logger.info("Received request to get messages.")
    try:
        async with httpx.AsyncClient() as client:
            logging_response = await client.get(f"{LOGGING_SERVICE_URL}/messages/")
            messages_response = await client.get(f"{MESSAGES_SERVICE_URL}/message/")
        logging_response.raise_for_status()
        messages_response.raise_for_status()
    except httpx.RequestError as exc:
        logger.error(f"Request to one of the services failed: {str(exc)}")
        raise HTTPException(status_code=500, detail=f"Request to one of the services failed: {str(exc)}")

    return {"logging_service": logging_response.text, "messages_service": messages_response.text}
