from fastapi import FastAPI
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="messages_service.log"
)
logger = logging.getLogger("messages_service")

app = FastAPI()


@app.get("/message/")
async def get_message():
    logger.info("Message service called - returning 'not implemented yet'.")
    return "not implemented yet"
