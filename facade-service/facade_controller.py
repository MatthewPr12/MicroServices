from fastapi import FastAPI, HTTPException, Body
import logging

from facade_service import FacadeService, httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(thread)d] - %(name)s - %(levelname)s - %(message)s",
    filename="facade_service.log"
)

logger = logging.getLogger("facade_service")

app = FastAPI()

facade_service = FacadeService()


@app.post("/post_message/")
async def post_message(msg: str = Body(...)):
    logger.info(f"Received message to log: {msg}")
    try:
        return await facade_service.add_message(msg)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Logging service request failed: {str(exc)}")


@app.get("/get_messages/")
async def get_messages():
    logger.info("Received request to get messages.")
    try:
        return await facade_service.get_messages()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Request to one of the services failed: {str(exc)}")
