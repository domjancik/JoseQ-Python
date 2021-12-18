import mido
import logging
import time

logger = logging.getLogger(__name__)

STEPS_COUNT = 16
# Tracks defined as tuples (name, note, channel)
TRACKS = [
    ('1', 60, 0),
    ('2', 63, 0),
    ('3', 66, 0),
    ('4', 69, 0),
    ('5', 72, 0),
    ('6', 75, 0)
]

class Track():
    def __init__(self, port, note: int, channel: int = 0, name: str = '') -> None:
        self.note = note
        self.channel = channel
        self.steps = [False]*STEPS_COUNT
        self.port = port
        self.name = name

    def play(self, step_index: int):
        assert step_index < STEPS_COUNT
        if self.steps[step_index]:
            self._play_midi()

    def set_steps(self, steps: list[bool]):
        assert len(steps) == STEPS_COUNT, f"Step count mismatch when updating track {self.name}"
        self.steps = steps
        logger.debug(f"Track {self.name} - Updated steps to {steps}")

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
        self.step = (self.step + 1) % STEPS_COUNT
        logger.debug(f"Current step: {self.step}")

    def step_time(self):
        return 1 / self.tempo * 16 
    
    def stop(self):
        if not self.is_playing:
            logger.debug("Resetting step to 0")
            self.step = 0

        logger.debug("Stopping playback")
        self.is_playing = False

    def set_track_steps(self, track_index: int, steps: list[bool]):
        assert track_index < len(self.tracks)
        self.tracks[track_index].set_steps(steps)
        self._touch()

    def set_tempo(self, tempo: int):
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


    