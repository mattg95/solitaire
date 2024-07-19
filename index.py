import random
import argparse

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


 

class Card():
    def __init__(self, suit, value, visible):
        self.suit = suit
        self.value = value
        self.visible = visible
        super().__init__

    def __repr__(self):
        return f"{self.value} of {self.suit}, {self.visible}"



class Solitaire():
    def __init__(self):
        super().__init__
        self.card_deck = None
        self.piles = None

    def setup(self):

        self.card_deck: list[Card] = []
        self.piles: list[list[Card]]  = []

        self.__get_all_cards()

        self.__setup_piles()


    def __find_first_visible_card(self,pile_index):
        for card in self.piles[pile_index]:
            print(card)
            if card.visible:
                return  card
    
    def __determine_visible(self,index, max):

        if index == max:
            return True
        else:
            return False
        
    def __get_all_cards(self):
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, None)
                self.card_deck.append(card)

    def __setup_piles(self):
        for pile_index in range(0, 7):
            pile = []
            max = pile_index + 1

            for card_index in range(0, max):
                random_card = random.choice(self.card_deck)
                random_card.visible = self.__determine_visible(card_index, max -1)

                pile.append(random_card)
                
            self.piles.append(pile)

    def __get_elements_after_visible(self,pile_index):
        card = self.__find_first_visible_card(pile_index)
        cardIndex = self.piles[pile_index].index(card)

        if cardIndex == -1:
            return []  # No visible cards found
        return self.piles[pile_index][cardIndex + 1:] 
        
    

    def move_cards(self, current_pile_index, next_pile_index):
        # print(current_pile_index, next_pile_index)
        
        first_card = self.__find_first_visible_card(current_pile_index)
        print(first_card)
        first_card_index = self.piles[current_pile_index].index(first_card)

        second_card = self.piles[next_pile_index][-1]

        cards_to_move = self.__get_elements_after_visible(current_pile_index)

        # print(first_card, second_card)

        if self.__is_valid_move(first_card, second_card):
            del self.piles[current_pile_index][first_card_index:-1]
            self.piles[next_pile_index].append(cards_to_move)
        else:
            print('Invalid move')


    def __is_black_suit(self, card):
        return card.suit == 'Clubs' or card.suit == 'SPADES'

    def __is_opposite_colour(self, card_1, card_2):
        red_and_black = self.__is_black_suit(card_1) and not self.__is_black_suit(card_2)
        back_and_red = not self.__is_black_suit(card_1) and self.__is_black_suit(card_2)

        return red_and_black or back_and_red
    
    def __is_one_smaller_value(self, card_1, card_2):
        card_1_value_index = CARD_VALUES.index(card_1.value)
        card_1_value_index = CARD_VALUES.index(card_2.value)

        return card_1_value_index == card_1_value_index + 1
    
    def __is_valid_move(self, card_1, card_2):
        return self.__is_opposite_colour(card_1, card_2) and  self.__is_one_smaller_value(card_1, card_2)


    def display(self):
        for card in self.piles:
            print(card)

def main():
    parser = argparse.ArgumentParser(description="The index of the stack to take from, followed by the index of the stack to move to.")
    parser.add_argument('operation', choices=['move_cards', 'see_cards'], help="The operation to perform.")
    parser.add_argument('num1',nargs='?', type=int, help="The first stack.")
    parser.add_argument('num2',nargs='?', type=int, help="The second stack.")
    
    args = parser.parse_args()

    game = Solitaire()
    
    game.setup()

    if args.operation == 'see_cards':
        game.display()
    elif args.operation == 'move_cards':
        game.move_cards(args.num1, args.num2)
        game.display()

   
main()



        




