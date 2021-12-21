import mido
import logging
import time

from joseqio.serial_receiver import SerialReceiver

logger = logging.getLogger(__name__)

STEPS_COUNT = 16
# Tracks defined as tuples (name, note, channel, flash)
TRACKS = [
    ('1', [ 58 ], 0, True),
    ('2', [ 59 ], 0, True),
    ('3', [ 60 ], 0, True),
    ('4', [ 61 ], 0, True),
    ('5', [ 62, 63 ], 0, True),
    ('6', [ 64 ], 0, True)
]

class Track():
    def __init__(self, port, serial: SerialReceiver, notes: list[int], channel: int = 0, name: str = '', flash_on_play: bool = False) -> None:
        self.notes = notes
        self.channel = channel
        self.steps = [False]*STEPS_COUNT
        self.port = port
        self.name = name
        self.flash_on_play = flash_on_play
        self.serial = serial

    def play(self, step_index: int):
        assert step_index < STEPS_COUNT
        if self.steps[step_index]:
            self._play_midi(step_index)
            if (self.flash_on_play):
                self.serial.send("F")

    def set_steps(self, steps: list[bool]):
        assert len(steps) == STEPS_COUNT, f"Step count mismatch when updating track {self.name}"
        self.steps = steps
        logger.debug(f"Track {self.name} - Updated steps to {steps}")

    def _get_current_note(self, step_index: int):
        note_index = step_index % len(self.notes) 
        return self.notes[note_index]

    def _play_midi(self, step_index: int):
        note = self._get_current_note(step_index)
        msg = mido.Message('note_on', note=note, channel=self.channel)
        logger.debug(f"Sending MIDI message: {msg}")
        self.port.send(msg)

class MidiSequencer():
    def __init__(self, port, serial: SerialReceiver) -> None:
        self.step = 0
        self.tempo = 120
        self.is_playing = False
        self.tracks = [Track(port, serial, note, channel, name, flash) for (name, note, channel, flash) in TRACKS]
        self.serial = serial
        logger.debug(f"Initialised tracks: {self.tracks}")

    def play(self):
        self.is_playing = True
        logger.debug(f"Playing: {self.is_playing}")
        self._touch()
    
    def play_tracks(self):
        for track in self.tracks:
            track.play(self.step)

    def increment_step(self):
        if not self.is_playing:
            return
        self._set_step((self.step + 1) % STEPS_COUNT)
        logger.debug(f"Current step: {self.step}")

    def _set_step(self, step: int):
        self.step = step
        self.serial.send(f"S:{self.step}")

    def step_time(self):
        if self.tempo == 0:
            logger.warn("Tempo is 0")
            return 0.1
        return 1 / self.tempo * 16 
    
    def stop(self):
        if not self.is_playing:
            logger.debug("Resetting step to 0")
            self._set_step(0)

        logger.debug("Stopping playback")
        self.is_playing = False

    def set_track_steps(self, track_index: int, steps: list[bool]):
        assert track_index < len(self.tracks)
        self.tracks[track_index].set_steps(steps)
        self._touch()

    def set_tempo(self, tempo: int):
        if (tempo == 0):
            logger.debug("Ignoring command to set tempo to 0")
            return
        logger.debug(f"Setting tempo to: {tempo}")
        self.tempo = tempo
        self._touch()

    def _touch(self):
        # TODO stop if untouched
        pass

    def loop(self):
        if (self.is_playing):
            self.play_tracks()
        time.sleep(self.step_time())
        self.increment_step()


    