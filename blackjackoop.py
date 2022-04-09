from random import shuffle


# table created for game play

class Table(object):

    def __init__(self, player, funds=100):
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player(player, funds)
        self.table_setup()

    def table_setup(self):
        self.deck.shuffle()
        self.player.place_bet()
        self.deal_card(self.player)
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.cal_score(self.player) 
        self.cal_score(self.dealer)
        self.main()

    def main(self):
        while True:
            print()
            print(self)
            player_move = self.player.hit_or_stay()
            if player_move is True:
                self.deal_card(self.player)
                self.cal_score(self.player)
            elif player_move is False: 
                self.dealer_hit()

    def dealer_hit(self):
        score = self.dealer.score
        while True:
            if score < 17:
                self.deal_card(self.dealer)
                self.cal_score(self.dealer)
                print(self)
            elif score >= 17:
                self.check_final_score()

    def __str__(self):  
        dealer_hand = [card for card, value in self.dealer.hand]
        player_hand = [card for card, value in self.player.hand]
        print("Dealer hand : {}".format(dealer_hand))
        print("Dealer score : {}".format(self.dealer.score))
        print()
        print("{}'s hand : {}".format(self.player.name, player_hand))
        print("{}'s score : {}".format(self.player.name, self.player.score))
        print()
        print(("{}'s current bet: {}.".format(self.player.name, self.player.bet)))
        print("{}'s current bank: {}.".format(self.player.name, self.player.funds))
        print("-" * 40)
        return ''

    def deal_card(self, player):
        card = self.deck.stack.pop()
        player.hand.append(card)

    def cal_score(self, player):
        ace = False  
        score = 0
        for card in player.hand:
            if card[1] == 1 and not ace:
                ace = True
                card = ('A', 11)
            score += card[1]
        player.score = score
        if player.score > 21 and ace:
            player.score -= 10
            score = player.score
        self.check_win(score, player)
        return

    def check_win(self, score, player):
        if score > 21:
            print()
            print(self)
            print("{} busts".format(player.name))
            print()
            self.end_game()
        elif score == 21:
            print(self)
            print("{} blackjack!".format(player.name))
            try:  
                player.payout()
            except:
                pass
            self.end_game()
        else:
            return

    def check_final_score(self):

        dealer_score = self.dealer.score
        player_score = self.player.score

        if dealer_score > player_score:
            print("Dealer wins!")
            self.end_game()
        else:
            print("{} wins!".format(self.player.name))
            self.end_game()

    def end_game(self):

        bank = self.player.funds
        if bank >=10:
            again = input("Play Again (Y/N)? ")
            if again.lower().startswith('y'):
                self.__init__(self.player.name, funds=self.player.funds)
            elif again.lower().startswith('n'):
                exit(1)  
        elif bank < 10:
            print("You're Broke! Better luck next time!")
            exit(2)


class Dealer(object):

    def __init__(self):

        self.name = "Dealer"
        self.score = 0
        self.hand = []


class Player(Dealer):

    def __init__(self, name, funds, bet=0):
        super().__init__()
        self.name = name
        self.funds = funds
        self.bet = bet

    def place_bet(self, amount=100):
        self.funds -= amount
        self.bet += amount

    def payout(self):
        self.funds += (self.bet * 2)
        self.bet = 0

    @staticmethod
    def hit_or_stay():
        while True:
            choice = input("would you like to hit again? (Y/N)? ")
            if choice.lower().startswith('y'):
                return True
            elif choice.lower().startswith('n'):
                return False
            else:
                print("I didn't understand")
                continue


class Deck(object):

 
    #list of all the values and shuffles


    def __init__(self):

        # using 2 decks
        self.stack = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                      ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
                      ('J', 10), ('Q', 10), ('K', 10)] * 8
        self.shuffle()

    def shuffle(self):

        shuffle(self.stack)

    def deal_card(self):

        card = self.stack.pop()
        return card


def main():

    player_name = input("Welcome to the Table!  What's your name? ")
    Table(player_name)


if __name__ == '__main__':

    main()