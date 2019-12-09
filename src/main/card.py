from enum import Enum


class Suit(Enum):
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    NONE = 4

    def __str__(self) -> str:
        out = ""
        if self.value == Suit.SPADES.value:
            out = "s"
        elif self.value == Suit.HEARTS.value:
            out = "h"
        elif self.value == Suit.CLUBS.value:
            out = "c"
        elif self.value == Suit.DIAMONDS.value:
            out = "d"
        else:
            out = "NONE"
        return out


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

    def __str__(self) -> str:
        out = ""
        if self.value == Value.TWO.value:
            out = "2"
        elif self.value == Value.THREE.value:
            out = "3"
        elif self.value == Value.FOUR.value:
            out = "4"
        elif self.value == Value.FIVE.value:
            out = "5"
        elif self.value == Value.SIX.value:
            out = "6"
        elif self.value == Value.SEVEN.value:
            out = "7"
        elif self.value == Value.EIGHT.value:
            out = "8"
        elif self.value == Value.NINE.value:
            out = "9"
        elif self.value == Value.TEN.value:
            out = "T"
        elif self.value == Value.JACK.value:
            out = "J"
        elif self.value == Value.QUEEN.value:
            out = "Q"
        elif self.value == Value.KING.value:
            out = "K"
        elif self.value == Value.ACE.value:
            out = "A"
        return out


class Card():

    CONVERSION = 2

    def __init__(self, suit: Suit, val: Value) -> None:
        self.suit = suit
        self.val = val

    def __str__(self) -> str:
        return f"{self.val}{self.suit}"

    def get_val(self) -> int:
        return self.val.value + self.CONVERSION


if __name__ == '__main__':
    print(Card(Suit.CLUBS, Value.TEN))