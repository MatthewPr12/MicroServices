import hazelcast
import logging
import subprocess
import signal
import os

logger = logging.getLogger("logging_service")


class LoggingService:
    def __init__(self):
        print(os.getcwd())
        self.hazelcast_process = subprocess.Popen(["./../../hazelcast-5.3.6/bin/hz-start"])
        logger.info("Hazelcast node started.")
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.client = hazelcast.HazelcastClient(
            cluster_name="dev",
        )
        self.logged_messages = self.client.get_map("logging_map").blocking()

    def signal_handler(self, signum, frame):
        self.cleanup_hazelcast()

    def cleanup_hazelcast(self):
        if self.hazelcast_process:
            logger.info("Shutting down Hazelcast node.")
            self.hazelcast_process.terminate()
            self.hazelcast_process.wait()
            logger.info("Hazelcast node shutdown complete.")

    def log_message(self, uuid: str, message: str):
        self.logged_messages.put(uuid, message)
        logger.info(f"Logging message: {message} with UUID: {uuid}")
        print(f"Logging message: {message} with UUID: {uuid}")
        return {"status": "logged"}

    def get_messages(self):
        all_messages = []
        for key, value in self.logged_messages.entry_set():
            all_messages.append(value)
        logger.info("Returning all logged messages.")
        return " ".join(all_messages)
