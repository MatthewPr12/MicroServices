import httpx
import logging
from uuid import uuid4
from random import choice
import hazelcast


class FacadeService:
    def __init__(self):
        self.logging_service_urls = [
            "http://localhost:8002",
            "http://localhost:8003",
            "http://localhost:8004"
        ]
        self.messages_service_urls = [
            "http://localhost:8005",
            "http://localhost:8006",
        ]
        self.clients = [httpx.AsyncClient(base_url=url) for url in self.logging_service_urls]
        self.client = hazelcast.HazelcastClient(
            cluster_name="dev",
        )

        self.message_queue = self.client.get_queue("message_queue").blocking()

    async def add_message(self, msg: str):
        msg_uuid = str(uuid4())
        selected_client = choice(self.clients)
        try:
            response = await selected_client.post("/log/", json={'uuid': msg_uuid, 'message': msg})
            logging.info(f"Message with UUID {msg_uuid} added to the queue.")
            response.raise_for_status()
            log_response = response.text
        except httpx.RequestError as exc:
            logging.error(f"Logging service request failed: {str(exc)}")
            log_response = {"error": f"Logging service request failed: {str(exc)}"}

        try:
            await self.message_queue.put({'uuid': msg_uuid, 'message': msg})
            logging.info(f"Message with UUID {msg_uuid} added to the queue.")
            queue_response = {"status": "Message added to the queue", "uuid": msg_uuid}
        except Exception as exc:
            logging.error(f"Error putting message to the queue: {str(exc)}")
            queue_response = {"error": f"Error putting message to the queue: {str(exc)}"}

        return {
            "log_response": log_response,
            "queue_response": queue_response
        }

    async def get_messages(self):
        messages_service_url = choice(self.messages_service_urls)
        try:
            async with httpx.AsyncClient() as client:
                messages_response = await client.get(f"{messages_service_url}/messages/")
            messages_response.raise_for_status()

            async with httpx.AsyncClient() as client:
                logging_service_url = choice(self.logging_service_urls)
                logging_response = await client.get(f"{logging_service_url}/messages/")
            logging_response.raise_for_status()

            # Combine responses
            combined_response = {
                "messages_service": messages_response.json(),
                "logging_service": logging_response.json()
            }
            print(combined_response)
            return combined_response

        except httpx.RequestError as exc:
            logging.error(f"Request to one of the services failed: {str(exc)}")
            raise exc
