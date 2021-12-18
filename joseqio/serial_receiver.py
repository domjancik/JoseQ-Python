import logging
from typing import Any, Callable, Mapping
import serial
from joseqio.protocol import parse_message_tokens, tokenize_message
from time import sleep

logger = logging.getLogger(__name__)

# TODO set from config
PORT_NAME = 'COM2'
BAUD_RATE = 115200

class SerialReceiver():
    def __init__(self, receive_callback: Callable[[Mapping[str, Any]], Any]) -> None:
        self.receive_callback = receive_callback
        
    def run(self):
        with serial.Serial(PORT_NAME, BAUD_RATE, timeout=1) as ser:
            while True:
                if (ser.in_waiting > 0):
                    message_bytes: bytes = ser.readline()
                    message = message_bytes.decode('ascii')
                    logger.debug(f"Received serial message: {message}")

                    message_tokens = tokenize_message(message)
                    parsed_message = parse_message_tokens(message_tokens)
                    if self.receive_callback:
                        self.receive_callback(parsed_message)

                sleep(0.1)

