import logging
import threading
from time import sleep
import os
import sys
import mido
from dotenv import load_dotenv
from joseqio.sequencer_controller import SequencerController
from joseqio.serial_receiver import SerialReceiver
from sequencer.midi_sequencer import MidiSequencer

load_dotenv()
PORT_NAME = os.environ["JOSEQ_SERIALPORT"]
BAUD_RATE = int(os.environ["JOSEQ_SERIALBAUDRATE"]) 

logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=logging.DEBUG)
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
           try:
              controller.evaluate_command(key, value) 
           except AssertionError:
               logger.exception(f"Failed to evaluate command {key}:{value}")


    receiver = SerialReceiver(PORT_NAME, BAUD_RATE, serial_command_received)
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


