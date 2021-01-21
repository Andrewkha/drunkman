from random import shuffle
from queue import Queue
from typing import List


class DrunkerGeneralException(Exception):
    pass


class InvalidCardException(DrunkerGeneralException):
    pass


class PlayerOutOfCardsException(DrunkerGeneralException):
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

    def __repr__(self):
        return self.value


class Deck:

    def __init__(self):
        self.all_deck = []
        for card_type in range(4):
            for one_card in Card.possible_values:
                self.all_deck.append(Card(one_card))

    def shuffle(self):
        shuffle(self.all_deck)


class Player:

    def __init__(self):
        self.hand = Queue()

    def move(self):
        if not self.hand.empty():
            return self.hand.get()
        else:
            raise PlayerOutOfCardsException

    def take(self, cards: List[Card]):
        for card in cards:
            self.hand.put(card)


class Game:

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        deck = Deck()
        deck.shuffle()
        self.deck = deck.all_deck
        self.deal()

    def deal(self):
        self.player1.take(self.deck[0:len(self.deck) // 2])
        self.player2.take(self.deck[len(self.deck) // 2:len(self.deck) + 1])

    def play(self):
        bank = []
        step = 0
        while True:
            step += 1
            try:
                card1 = self.player1.move()
            except PlayerOutOfCardsException:
                print("Player 1 has lost the game")
                break

            try:
                card2 = self.player2.move()
            except PlayerOutOfCardsException:
                print("Player 2 has lost the game")
                break

            bank.append(card1)
            bank.append(card2)

            if card1 > card2:
                self.player1.take(bank)
                bank = []
            elif card2 > card1:
                self.player2.take(bank)
                bank = []
            elif card1 == card2:
                continue

        print(f"Number of steps: {step}")


if __name__ == "__main__":
    game = Game()

    game.play()
