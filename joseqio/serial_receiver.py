import logging
import os
from typing import Any, Callable, Mapping
import serial
from joseqio.protocol import parse_message_tokens, tokenize_message
from time import sleep

logger = logging.getLogger(__name__)

class SerialReceiver():
    def __init__(self, port_name: str, baud_rate: int, receive_callback: Callable[[Mapping[str, Any]], Any]) -> None:
        self.receive_callback = receive_callback
        self.port_name = port_name
        self.baud_rate = baud_rate
        
    def run(self):
        with serial.Serial(self.port_name, self.baud_rate, timeout=1) as ser:
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

                sleep(0.1)

