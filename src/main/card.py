from enum import Enum


class Suit(Enum):
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    NONE = 4


class Value(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12
    NONE = 13


class Card():

    CONVERSION = 2

    def __init__(self, suit: Suit, val: Value):
        self.suit = suit
        self.val = val

    def __str__(self):
        return f"{self.val.name} of {self.suit.name}"

    def get_val(self) -> int:
        return self.val.value + self.CONVERSION


if __name__ == '__main__':
    print(Card(Suit.CLUBS, Value.TEN))