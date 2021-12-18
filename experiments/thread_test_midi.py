
import threading
from random import randint
from time import sleep
import mido

BLURBS = [
"Ahh, there's this one thing...",
"A-hem",
"Indeed",
"Two may be too much",
"What a day today, huh?"
]

global said
said = (0, 'Init') 


outputs = mido.get_output_names()
port = mido.open_output(outputs[0])

def talker_function():
    last_read_index = 0
    while True:
        print(BLURBS[randint(0, len(BLURBS)-1)])
        global said
        index, message = said
        if index > last_read_index:
            last_read_index = index
            print(f"Also, you said: {message}")
            # Avoid writing to same variable from two places. Although this might not be needed due to GIL.
            # said = None

        sleep(randint(1, 4))

def play_function(interval, note):
    while True:
        print(f"Playing {note} for {interval}s")
        msg = mido.Message('note_on', note=note)
        port.send(msg)
        sleep(interval)


if __name__ == "__main__":
    # talker = threading.Thread(target=talker_function)
    # talker.start()
    def play(interval, note):
        player = threading.Thread(target=play_function, args=[interval, note])
        player.start()

    play(1, 60)
    play(0.7, 63)
    play(0.4, 65)

    print("Started!")

    while True:
        message = input("Tell me things:")
        index, _ = said
        said = (index + 1, message)
        # Needs queue, messages may be missed