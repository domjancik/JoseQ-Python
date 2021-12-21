import logging
import queue
from typing import Any, Callable, Mapping
import serial
from joseqio.protocol import parse_message_tokens, tokenize_message
from time import sleep

logger = logging.getLogger(__name__)

class SerialReceiver():
    def __init__(self, port_name: str, baud_rate: int) -> None:
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.command_queue: queue.Queue[str] = queue.Queue()

    def set_callback(self, receive_callback: Callable[[Mapping[str, Any]], Any]):
        self.receive_callback = receive_callback

    def send(self, command: str):
        if self.command_queue.qsize() > 5:
            logger.warn(f"Too many commands in queue, ignoring command {command}")

        self.command_queue.put(command)
        
    def run(self):
        with serial.Serial(self.port_name, self.baud_rate, timeout=1) as ser:
            logger.info(f"Connected to Serial: {self.port_name} at baud rate {self.baud_rate}")
            while True:
                if (ser.in_waiting > 0):
                    message_bytes: bytes = ser.readline()
                    try:
                        message = message_bytes.decode('utf8')
                        logger.debug(f"Received serial message: {message}")

                        message_tokens = tokenize_message(message)
                        parsed_message = parse_message_tokens(message_tokens)
                        if self.receive_callback:
                            self.receive_callback(parsed_message)
                    except UnicodeDecodeError:
                        logger.exception(f"Failed to decode Serial input - {message_bytes}")

                while self.command_queue.qsize():
                    logger.debug(f"Commands in queue: {self.command_queue.qsize()}")
                    command = self.command_queue.get()
                    logger.debug(f"Sending command: {command}")
                    ser.write(f"{command}\n".encode('ascii'))
                sleep(0.05)

