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

        def set_track_steps(track_index: int):
            def inner(value):
                sequencer.set_track_steps(track_index, value)

            return inner

        def set_track_velocity(track_index: int, note_index: int = 0):
            def inner(value):
                sequencer.set_track_velocity(track_index, value, note_index)

            return inner
            
        self.command_handlers = {
            "PLAY": conditionally_do(sequencer.play),
            "STOP": conditionally_do(sequencer.stop),
            "TEMPO": sequencer.set_tempo,
            "CAL1": set_track_velocity(0),
            "CAL2": set_track_velocity(1),
            "CAL3": set_track_velocity(2),
            "CAL4": set_track_velocity(3),
            "CAL5": set_track_velocity(4, 0),
            "CAL6": set_track_velocity(4, 1),
            "CAL7": set_track_velocity(5),
            "ROW1": set_track_steps(0),
            "ROW2": set_track_steps(1),
            "ROW3": set_track_steps(2),
            "ROW4": set_track_steps(3),
            "ROW5": set_track_steps(4),
            "ROW6": set_track_steps(5)
        }

    def evaluate_command(self, key: str, value):
        def unknown_handler(_):
            logger.debug(f"Received unknown command: {key}:{value}")

        handler = self.command_handlers.get(key, unknown_handler)
        handler(value)