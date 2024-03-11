import httpx
import logging
from uuid import uuid4
from random import choice


class FacadeService:
    def __init__(self):
        self.logging_service_urls = [
            "http://localhost:8002",
            "http://localhost:8003",
            "http://localhost:8004"
        ]
        self.message_service_url = "http://localhost:8001"
        self.clients = [httpx.AsyncClient(base_url=url) for url in self.logging_service_urls]

    async def add_message(self, msg: str):
        msg_uuid = str(uuid4())
        selected_client = choice(self.clients)
        try:
            response = await selected_client.post("/log/", json={'uuid': msg_uuid, 'message': msg})
            response.raise_for_status()
            return response.text
        except httpx.RequestError as exc:
            logging.error(f"Logging service request failed: {str(exc)}")
            return {"error": str(exc)}

    async def get_messages(self):
        selected_client = choice(self.clients)
        try:
            logging_response = await selected_client.get("/messages/")
            # Assuming that the messages service is different and not included in the round-robin
            async with httpx.AsyncClient(base_url=self.message_service_url) as message_client:
                messages_response = await message_client.get("/message/")

            logging_response.raise_for_status()
            messages_response.raise_for_status()
            return {"logging_service": logging_response.text, "messages_service": messages_response.text}
        except httpx.RequestError as exc:
            logging.error(f"Request to one of the services failed: {str(exc)}")
            raise exc  # This will be caught by the FastAPI exception handler
