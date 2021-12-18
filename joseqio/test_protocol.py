import unittest

from joseqio.protocol import parse_message_tokens, tokenize_message

class TestTokenizeMessage(unittest.TestCase):
    def test_should_parse_single_keyvalue_pair_in_line(self):
        message = "KEY:VALUE"
        result = tokenize_message(message)
        expected = {
            "KEY": "VALUE"
        }
        self.assertEqual(result, expected)

    def test_should_parse_multiple_keyvalue_pairs_per_line(self):
        message = "KEY:VALUE ANOTHER:ONE"
        result = tokenize_message(message)
        expected = {
            "KEY": "VALUE",
            "ANOTHER": "ONE"
        }
        self.assertEqual(result, expected)

class TestParseMessageTokens(unittest.TestCase):
    def test_should_parse_play_message_as_boolean(self):
        tokens = {
            "PLAY": "1"
        }
        result = parse_message_tokens(tokens)
        expected = {
            "PLAY": True
        }
        self.assertEqual(result, expected)

    def test_should_parse_stop_message_as_boolean(self):
        tokens = {
            "STOP": "0"
        }
        result = parse_message_tokens(tokens)
        expected = {
            "STOP": False 
        }
        self.assertEqual(result, expected)

    def test_should_parse_row_message_as_array(self):
        tokens = {
            "ROW1": "0101|1111|0000|1010"
        }
        result = parse_message_tokens(tokens)
        expected = {
            "ROW1": [False,True,False,True,True,True,True,True,False,False,False,False,True,False,True,False] 
        }
        self.assertEqual(result, expected)

    def test_should_parse_tempo_message_as_int(self):
        tokens = {
            "TEMPO": "120"
        }
        result = parse_message_tokens(tokens)
        expected = {
            "TEMPO": 120 
        }
        self.assertEqual(result, expected)