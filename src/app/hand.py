from enum import Enum

from src.app.card import Card, Suit, Value, MAX_VALUE

class Result(Enum):
    WIN = 0
    LOSE = 1
    TIE = 2


class Play(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    NONE = 9


class Hand():
    def __init__(self, cards: set) -> None:
        self.cards = cards if len(cards) == 5 else set() 
        self.play = Play.NONE
        self.value = 0

    def __repr__(self) -> str:
        return self.representation()

    def __str__(self) -> str:
        return self.representation()

    def representation(self) -> str:
        tmp = "["
        for card in self.cards:
            tmp += f"| {card.__str__()} "

        tmp = tmp.replace("|", "", 1)
        tmp += f"]  =>  {self.play.name}"
        return tmp

    def compare(self, hand) -> Result:
        """
        States whether self wins, losses or ties against hand
        """
        if self.play.value > hand.play.value:
            return Result.WIN
        elif self.play.value < hand.play.value:
            return Result.LOSE
        else:
            if self.value == hand.value:
                return Result.TIE

            return Result.WIN if self.value > hand.value else Result.LOSE


def classify(hand: Hand) -> dict:
    """
    Takes a hand obj and classifies its cards in order to see which values
    are repeated.
    """
    classification = {v : 0 for v in range(Value.ACE.value+1)}
    for card in hand.cards:
        classification[card.val.value] += 1 

    return classification

def get_combined_play(n: int, m: int, classification: dict) -> int:
    """
    Takes two int values and a dict returned by classify method.
    Int values are used to look for repeated cards.
    E.g. if you call get_combined_play(2, 2, c), you'll look for two pair.
    if you call get_combined_play(4, 0, c), you'll look for four of a kind.

    returns a value>0 which is the score of the play
    returns 0 if it couldn't find the play
    """
    times_updated_first = 0
    times_updated_second = 0
    val = 0

    for k in classification.keys():
        if classification[k] == n:
            val += (k + Card.CONVERSION) * n
            times_updated_first += 1
        elif classification[k] == m:
            val += (k + Card.CONVERSION) * m
            times_updated_second += 1

    if n == m and times_updated_first == 2:
        return val
    elif not(n==m) and times_updated_first >= 1 and times_updated_second >= 1:
        return val
    else:
        return 0

def get_straight(classification: dict) -> int:
    """
    returns a value>0 which is the score of the play
    returns 0 if it couldn't find the play
    """
    val = 0
    followers = 0
    for i in range(Value.ACE.value+1):
        if followers and not classification[i]:
            val = 0
            followers = 0
            break
        if classification[i]:
            val += i + Card.CONVERSION
            followers += 1
        if followers == 5:
            return val

    if not val:
        for i in range(Value.ACE.value, Value.ACE.value*2+1):
            if followers and not classification[i % MAX_VALUE]:
                return 0
            if classification[i % MAX_VALUE]:
                val += i % MAX_VALUE + Card.CONVERSION
                followers += 1
            if followers == 5:
                return val

    return val

def get_flush(hand: Hand) -> int:
    """
    returns a value>0 which is the score of the play
    returns 0 if it couldn't find the play
    """
    cards = list(hand.cards)
    val = cards[0].get_val()
    suit = cards[0].suit
    for i in range(1, len(cards)):
        if not(cards[i].suit == suit):
            return 0
        val += cards[i].get_val()
        
    return val

def get_high_card(hand: Hand) -> int:
    """
    returns the highest card value in the hand
    """
    return max(hand.cards, key=Card.get_val).get_val()

def calculate_play_hand(hand: Hand):
    """
    calculates the hand play and its value 
    """
    classification = classify(hand)

    # Straight flush
    s_val = get_straight(classification)
    f_val = get_flush(hand)
    if s_val and f_val:
        hand.play = Play.STRAIGHT_FLUSH
        hand.value = s_val + f_val
        return

    # four of a kind
    val = get_combined_play(4, 0, classification)
    if val:
        hand.play = Play.FOUR_OF_A_KIND
        hand.value = val
        return

    # full house
    val = get_combined_play(3, 2, classification)
    if val:
        hand.play = Play.FULL_HOUSE
        hand.value = val
        return
    # flush
    if f_val:
        hand.play = Play.FLUSH
        hand.value = f_val
        return
    # straight
    if s_val:
        hand.play = Play.STRAIGHT
        hand.value = s_val
        return
    # three of a kind
    val = get_combined_play(3, 0, classification)
    if val:
        hand.play = Play.THREE_OF_A_KIND
        hand.value = val
        return
    # two pair
    val = get_combined_play(2, 2, classification)
    if val:
        hand.play = Play.TWO_PAIR
        hand.value = val
        return
    # pair
    val = get_combined_play(2, 0, classification)
    if val:
        hand.play = Play.PAIR
        hand.value = val
        return
    # high card
    hand.play = Play.HIGH_CARD
    hand.value = get_high_card(hand)


if __name__ == '__main__':
    hand = Hand([Card(Suit.CLUBS, Value.TEN), 
    Card(Suit.CLUBS, Value.EIGHT), 
    Card(Suit.HEARTS, Value.TEN), 
    Card(Suit.SPADES, Value.EIGHT), 
    Card(Suit.CLUBS, Value.ACE)])

    calculate_play_hand(hand)

    print(hand)
