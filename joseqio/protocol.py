from typing import Mapping
import re
import functools


def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose2, functions, lambda x: x)


REGEX = "([^\s]+):([^\s]+)"
def tokenize_message(message: str) -> Mapping[str, str]:
    """
    Parse key-value pairs from a string message into a dict
    """
    found_tokens = re.findall(REGEX, message)
    return {k:v for (k,v) in found_tokens} 
 
_str_to_bool = compose(bool, int)
def _map_row(value: str):
    meaningful_values = re.sub("[^01]", "", value)
    return [_str_to_bool(v) for v in meaningful_values] 
VALUE_MAPPERS = {
    "PLAY": _str_to_bool,
    "STOP": _str_to_bool,
    "TEMPO": int,
    "ROW1": _map_row,
    "ROW2": _map_row,
    "ROW3": _map_row,
    "ROW4": _map_row,
    "ROW5": _map_row,
    "ROW6": _map_row
}

    
def parse_message_tokens(message_tokens: Mapping[str, str]):
    def map_value(key, value):
        return VALUE_MAPPERS[key](value)

    return {k:map_value(k, v) for (k, v) in message_tokens.items()}