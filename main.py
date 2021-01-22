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

    def __init__(self, id_=1, write_log=False):
        self.game_id = id_
        self.write_log = write_log
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
        log_messages = []

        while True:
            step += 1

            log_messages.append(f"Step: {step}")
            log_messages.append(f"Player1 hand before step {self.player1.hand.queue}")
            log_messages.append(f"Player2 hand before step {self.player2.hand.queue}")

            try:
                card1 = self.player1.move()
                log_messages.append(f"Player1 puts {card1}")
            except PlayerOutOfCardsException:
                log_messages.append("Player1 lost the game")
                if self.write_log and step <= 19:
                    with open(f'log/game_{self.game_id}.txt', 'w') as file_:
                        file_.write('\n'.join(log_messages))
                # print("Player 1 has lost the game")
                # print(f"Game {self.game_id} finished. Steps {step}")
                return 2, step, self.game_id

            try:
                card2 = self.player2.move()
                log_messages.append(f"Player2 puts {card2}")
            except PlayerOutOfCardsException:
                log_messages.append("Player 2 has lost the game")
                if self.write_log and step <= 19:
                    with open(f'log/game_{self.game_id}.txt', 'w') as file_:
                        file_.write('\n'.join(log_messages))
                # print(f"Game {self.game_id} finished. Steps {step}")
                return 1, step, self.game_id

            bank.append(card1)
            bank.append(card2)

            shuffle(bank)

            log_messages.append(f"Bank: {bank}")

            if card1 > card2:
                self.player1.take(bank)
            elif card2 > card1:
                self.player2.take(bank)
            elif card1 == card2:
                log_messages.append('Spor!')
                continue
            bank = []

            log_messages.append(f"Player1 hand after step {self.player1.hand.queue}")
            log_messages.append(f"Player2 hand after step {self.player2.hand.queue}")
            log_messages.append("-------------------------------------------------")


if __name__ == "__main__":

    wins = []
    steps = []
    shortest = []
    for k in range(100000):
        game = Game(id_=k, write_log=True).play()
        wins.append(game[0])
        steps.append(game[1])
        if game[1] <= 19:
            shortest.append(game[2])

    print(wins.count(1), wins.count(2), wins.count(3), max(steps), min(steps), sum(steps) / len(steps))
    print(f"Short games: {shortest}")
