import unittest
from hypothesis import given, example, Verbosity, settings
from hypothesis.strategies import text

def encode(input_string):
    if not input_string:
        return []

    count = 1
    prev = ""
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            #count = 1  #ERROR
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst


def decode(lst):
    q = ""
    for character, count in lst:
        q += character * count
    return q


class TestEncoding(unittest.TestCase):

    @given(text())
    @example(s="")
    @settings(verbosity=Verbosity.verbose)
    def test_decode_inverts_encode(self, s):
        self.assertEqual(decode(encode(s)), s)


if __name__ == "__main__":
    unittest.main()