from random import shuffle


class DrunkerGeneralException(Exception):
    pass


class InvalidCardException(DrunkerGeneralException):
    pass


class Card:

    possible_values = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, value):
        if value in self.possible_values:
            self.value = value
        else:
            raise InvalidCardException

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        if self.value == '6' and other.value == 'A':
            return True
        if self.possible_values.index(self.value) > self.possible_values.index(other.value) and \
                (self.value != 'A' or other.value != '6'):
            return True
        return False


class Deck:

    def __init__(self):
        self.all_deck = []
        for card_type in range(4):
            for one_card in Card.possible_values:
                self.all_deck.append(Card(one_card))

    def shuffle(self):
        shuffle(self.all_deck)
