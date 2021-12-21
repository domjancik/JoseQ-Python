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
MIDI_PATTERN = os.environ["JOSEQ_MIDI_PATTERN"]

logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=logging.DEBUG)
logger = logging.getLogger(__name__)

def sequencer_function(sequencer: MidiSequencer):
    logger.info("Sequencer thread started")
    # for i in range(6):
    #     sequencer.set_track_steps(i, [True, False]*8)
    #     if (i == 4):
    #         sequencer.set_track_steps(i, [True]*16)
    # sequencer.play()
    while True:
        sequencer.loop()

# TODO rename receiver to Communicator or similar
def serial_function(serial: SerialReceiver, sequencer: MidiSequencer):
    logger.info("Serial thread started")
    controller = SequencerController(sequencer) 
    def serial_command_received(commands):
        for (key, value) in commands.items():
           try:
              controller.evaluate_command(key, value) 
           except AssertionError:
               logger.exception(f"Failed to evaluate command {key}:{value}")


    serial.set_callback(serial_command_received)
    serial.run()

if __name__ == '__main__':
    outputs = mido.get_output_names()
    logger.debug(f"MIDI: Got outputs: {outputs}")
    # TODO Port selection via config
    output_name = None
    for name in outputs:
        if MIDI_PATTERN in name:
            output_name = name
            break

    if output_name is None:
        logger.error("No output matching MIDI_PATTERN found, exiting")
        exit(1)
            
    port = mido.open_output(output_name)
    logger.debug(f"MIDI: Got port: {port}")

    serial = SerialReceiver(PORT_NAME, BAUD_RATE)
    sequencer = MidiSequencer(port, serial)

    sequencer_thread = threading.Thread(target=sequencer_function, args=[sequencer], daemon=True)
    serial_thread = threading.Thread(target=serial_function, args=[serial, sequencer], daemon=True)

    sequencer_thread.start()
    serial_thread.start()

    while True:
        sleep(10)


