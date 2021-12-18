import logging
from typing import Callable

from sequencer.midi_sequencer import MidiSequencer


logger = logging.getLogger(__name__)

class SequencerController():
    def __init__(self, sequencer: MidiSequencer) -> None:
        self.sequencer = sequencer
        def conditionally_do(callback: Callable):
            def inner(value):
                if value:
                    callback()

            return inner

        self.command_handlers = {
            "PLAY": conditionally_do(sequencer.play),
            "STOP": conditionally_do(sequencer.stop)
        }

    def evaluate_command(self, key: str, value):
        def unknown_handler(_):
            logger.debug(f"Received unknown command: {key}:{value}")

        handler = self.command_handlers.get(key, unknown_handler)
        handler(value)