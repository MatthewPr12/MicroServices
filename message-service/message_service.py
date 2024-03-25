import hazelcast
import logging
from threading import Thread, Lock

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(thread)d] - %(name)s - %(levelname)s - %(message)s",
    filename="messages_service.log"
)
logger = logging.getLogger("messages_service")


class MessageService:
    def __init__(self):
        self.client = hazelcast.HazelcastClient(
            cluster_name="dev",
        )
        self.message_queue = self.client.get_queue("message_queue").blocking()
        self.local_message_store = []
        self.store_lock = Lock()  # mutex
        self.consumer_thread = Thread(target=self.consume_messages, daemon=True)
        self.consumer_thread.start()

    def get_messages(self):
        with self.store_lock:
            return list(self.local_message_store)

    def consume_messages(self):
        while True:
            try:
                message = self.message_queue.take()
                with self.store_lock:
                    self.local_message_store.append(message)
                logger.info(f"Consumed message: {message}")
            except Exception as e:
                logger.error(f"Error consuming messages: {e}")
            # TODO: Consider implementing a sleep or pause mechanism to prevent a tight loop

    def stop_consuming(self):
        if self.client:
            self.client.shutdown()


message_service = MessageService()
