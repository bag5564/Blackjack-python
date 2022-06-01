from player import Player
from dealer import Dealer


class BlackjackGame:
    def __init__(self, player_names):
        self.dealer = Dealer()
        self.player_list = []
        for name in player_names:
            self.player_list.append(Player(name, self.dealer))
        return None

    def play_rounds(self, num_rounds=1):
        """
        >>> import random; random.seed(1)
        >>> game = BlackjackGame(["Lawrence","Melissa"])
        >>> print(game.play_rounds(2))
        Round 1
        Dealer: [10, 9] 0/0/0
        Lawrence: [10, 6, 3] 0/1/0
        Melissa: [8, 8] 0/0/1
        Round 2
        Dealer: [10, 10] 0/0/0
        Lawrence: [10, 3] 0/1/1
        Melissa: [9, 10] 0/0/2
        >>> game = BlackjackGame(["Lawrence","Melissa","Ben","Fabi"])
        >>> print(game.play_rounds(4))
        Round 1
        Dealer: [8, 7, 5] 0/0/0
        Lawrence: [6, 10, 10] 0/0/1
        Melissa: [7, 11, 2, 6] 0/0/1
        Ben: [4, 9, 10] 0/0/1
        Fabi: [4, 10, 10] 0/0/1
        Round 2
        Dealer: [3, 10, 10] 0/0/0
        Lawrence: [7, 4, 8] 1/0/1
        Melissa: [9, 10] 1/0/1
        Ben: [9, 6, 5] 1/0/1
        Fabi: [11, 2] 1/0/1
        Round 3
        Dealer: [10, 10] 0/0/0
        Lawrence: [9, 5, 10] 1/0/2
        Melissa: [5, 10, 10] 1/0/2
        Ben: [10, 10] 1/1/1
        Fabi: [11, 6, 2, 8] 1/0/2
        Round 4
        Dealer: [8, 6, 4] 0/0/0
        Lawrence: [9, 6] 1/0/3
        Melissa: [5, 7, 3, 10] 1/0/3
        Ben: [9, 4, 7, 6] 1/1/2
        Fabi: [10, 10] 2/0/2
        """

        results = ""
        currentRound = 1

        while currentRound <= num_rounds:
            # list of players that get a natural blackjack or bust early in the round (after 2 cards)
            earlyFinishers = []

            # shuffle
            self.dealer.shuffle_deck()

            # Deal two cards to players and dealer
            for i in range(0,2,):
                for person in self.player_list:
                    self.dealer.signal_hit(person)
                self.dealer.signal_hit(self.dealer)

            # If dealer has Natural Blackjack, the current round ends
            if self.dealer.card_sum == 21:
              for person in self.player_list:
                if person.card_sum == 21:
                  person.record_tie()
                else:
                  person.record_loss()

            else:
              # Each person play round if they don't have a Natural Blackjack or have already busted
              for person in self.player_list:
                  # check if person has a Natural Blackjack
                  if person.card_sum == 21:
                    earlyFinishers.append(person.name)
                    person.record_win()
                  # check if person already busted
                  elif person.card_sum > 21:
                    earlyFinishers.append(person.name)
                    person.record_loss()
                  else:
                    person.play_round()
              # Dealer plays round (only if there are players that haven't finished early)
              if len(self.player_list) > len(earlyFinishers):
                self.dealer.play_round()

              # Calculate each person result
              for person in self.player_list:
                # Do calculation only if person didn't finish early
                if person.name not in earlyFinishers:
                  if person.card_sum > 21 or (self.dealer.card_sum <= 21 and person.card_sum < self.dealer.card_sum):
                    person.record_loss()
                  elif person.card_sum == self.dealer.card_sum:
                    person.record_tie()
                  else:
                    person.record_win()

            # Summarize results and discard cards
            results += 'Round ' + str(currentRound)  +'\n'
            results +=  str(self.dealer)
            for person in self.player_list:
              results +=  '\n' + str(person)
              person.discard_hand()
            self.dealer.discard_hand()

            if currentRound !=  num_rounds:
                results += '\n'
            currentRound += 1
        return results


    def reset_game(self):
        """
        >>> game = BlackjackGame(["Lawrence", "Melissa"])
        >>> _ = game.play_rounds()
        >>> game.reset_game()
        >>> game.player_list[0]
        Lawrence: [] 0/0/0
        >>> game.player_list[1]
        Melissa: [] 0/0/0
        """
        for person in self.player_list:
            person.reset_stats()
            person.discard_hand()

        return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
