import threading
from random import randint
from time import sleep

BLURBS = [
"Ahh, there's this one thing...",
"A-hem",
"Indeed",
"Two may be too much",
"What a day today, huh?"
]

global said
said = (0, 'Init') 

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

if __name__ == "__main__":
    talker = threading.Thread(target=talker_function)
    talker.start()
    print("Started!")

    while True:
        message = input("Tell me things:")
        index, _ = said
        said = (index + 1, message)
        # Needs queue, messages may be missed