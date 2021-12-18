import logging
import threading
from time import sleep
from joseqio.sequencer_controller import SequencerController
from joseqio.serial_receiver import SerialReceiver
import mido
from sequencer.midi_sequencer import MidiSequencer

logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.DEBUG)
logger = logging.getLogger(__name__)

def sequencer_function(sequencer: MidiSequencer):
    logger.info("Sequencer thread started")
    while True:
        sequencer.loop()

def serial_function(sequencer: MidiSequencer):
    logger.info("Serial thread started")
    controller = SequencerController(sequencer) 
    def serial_command_received(commands):
        for (key, value) in commands.items():
           controller.evaluate_command(key, value) 

    receiver = SerialReceiver(serial_command_received)
    receiver.run()

if __name__ == '__main__':
    outputs = mido.get_output_names()
    logger.debug(f"MIDI: Got outputs: {outputs}")
    # TODO Port selection via config
    port = mido.open_output(outputs[0])
    logger.debug(f"MIDI: Got port: {port}")

    sequencer = MidiSequencer(port)

    sequencer_thread = threading.Thread(target=sequencer_function, args=[sequencer], daemon=True)
    serial_thread = threading.Thread(target=serial_function, args=[sequencer], daemon=True)

    sequencer_thread.start()
    serial_thread.start()

    while True:
        sleep(10)


