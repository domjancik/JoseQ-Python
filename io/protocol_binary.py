# DEPRECATED
from typing import Iterable

def decode_sequencer_state():
    pass

def decode_track_bytes():
    pass

def byte_to_bit_bool_array(b: int) -> Iterable[bool]:
    bool_array = [False] * 8
    for i in range(8):
        bool_array[i] = extract_bit_bool(b, i)

    return bool_array

def extract_bit_bool(b: int, index: int) -> bool:
    return True if (b >> index & 1) == 1 else False