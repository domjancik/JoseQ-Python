import mido
import logging
import time

logger = logging.getLogger(__name__)

STEPS_COUNT = 16
# Tracks defined as tuples (name, note, channel)
TRACKS = [
    ('1', 60, 0)
]

class Track():
    def __init__(self, port, note: int, channel: int = 0, name: str = '') -> None:
        self.note = note
        self.channel = channel
        self.steps = [False]*STEPS_COUNT
        self.port = port

    def play(self, step_index: int):
        assert step_index < STEPS_COUNT
        if self.steps[step_index]:
            self._play_midi()

    def _play_midi(self):
        msg = mido.Message('note_on', note=self.note, channel=self.channel)
        logger.debug(f"Sending MIDI message: {msg}")
        self.port.send(msg)

class MidiSequencer():
    def __init__(self, port) -> None:
        self.step = 0
        self.tempo = 120
        self.is_playing = False
        self.tracks = [Track(port, note, channel, name) for (name, note, channel) in TRACKS]

    def play(self):
        self.is_playing = True
        logger.debug(f"Playing: {self.is_playing}")
    
    def play_tracks(self):
        for track in self.tracks:
            track.play(self.step)

    def increment_step(self):
        if not self.is_playing:
            return
        self.step = (self.step + 1) % STEPS_COUNT
        logger.debug(f"Current step: {self.step}")

    def step_time(self):
        return 1 / self.tempo * 16 
    
    def stop(self):
        if not self.is_playing:
            self.step = 0

        self.is_playing = False

    def loop(self):
        if (self.is_playing):
            self.play_tracks()
        time.sleep(self.step_time())
        self.increment_step()


    