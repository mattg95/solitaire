import random
import argparse
import pickle
import os


CARD_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

type Pile = list[list[Card]]

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.visible = None
        super().__init__

    def get_value(self):
        return CARD_RANKS.index(self.rank)

    def display(self):
        return (self.rank + " of " + self.suit)
    
class Piles():
    def __init__(self, card_deck):
        self.piles: Pile = []
        self.__setup_piles(card_deck)     
        super().__init__

    def __setup_piles(self, card_deck):
        for pile_index in range(0, 7):
            pile = []
            max = pile_index + 1

            for _ in range(0, max):
                random_card = random.choice(card_deck)
                card_deck.remove(random_card)
                random_card.visible = False

                pile.append(random_card)
            
            pile[max-1].visible = True

            self.piles.append(pile)

class CardDeck():
    def __init__(self):
        self.card_deck: list[Card] = []
        
        self.__get_all_cards()
        super().__init__

    def __get_all_cards(self):
        for card_suit in CARD_SUITS:
            for card_rank in CARD_RANKS:
                card = Card(card_suit, card_rank)
                self.card_deck.append(card)

class Foundations():
    def __init__(self):
        self.foundations: Pile = [[],[],[],[]]
        super().__init__

    def move_card(self, foundations, piles, pile_index: int, foundation_index: int):
        card = piles[pile_index][-1]
        is_same_suit = CARD_SUITS.index(card.suit) == foundation_index
        

        def excecute_swap():
            foundations[foundation_index].append(card)
            del piles[pile_index][-1]
            piles[pile_index][-1].visible = True
            return True


        if not foundations[foundation_index] and card.rank == 'A' and is_same_suit:
            return excecute_swap()
        else:
            last_card_in_foundation = foundations[foundation_index][-1]
            is_one_less = last_card_in_foundation.getValue() == card.getValue() - 1

            if  is_one_less and is_same_suit:
                return excecute_swap()

            else:
                print('invalid move')


class Solitaire():
    def __init__(self):
        super().__init__
        self.card_deck = None
        self.piles = None
        self.foundations = None

    def setup(self):

        self.card_deck = CardDeck().card_deck
        self.piles = Piles(self.card_deck).piles
        self.foundations = Foundations().foundations

        self.save_state()

    def __check_game_win(self):
        if all(not foundation for (foundation) in self.foundations):
            print("GAME WON!!!")


    def __find_first_visible_card(self,pile_index):
        for card in self.piles[pile_index]:
            if card.visible:
                return  card
        return None
    
    def __find_first_visible_card_index(self,pile_index):
        for index, card in enumerate(self.piles[pile_index]):
            if card.visible:
                return index



    def __get_elements_after_visible(self,pile_index):
        card_index = self.__find_first_visible_card_index(pile_index)

        if card_index == -1:
            return []  # No visible cards found
        return self.piles[pile_index][card_index:] 
        
    

    def move_cards(self, current_pile_index, next_pile_index):
        
        first_card = self.__find_first_visible_card(current_pile_index)
        first_card_index = self.piles[current_pile_index].index(first_card)

        second_card = self.piles[next_pile_index][-1]

        cards_to_move = self.__get_elements_after_visible(current_pile_index)

        if self.__is_valid_move(first_card, second_card) or self.__is_moving_to_empty_foundation(first_card, second_card):
            del self.piles[current_pile_index][first_card_index:]
            self.piles[current_pile_index][first_card_index -1].visible = True
            self.piles[next_pile_index].extend(cards_to_move)
            print("Moved: ", cards_to_move, " TO ", self.piles[next_pile_index])
            self.__display_card(first_card)
            self.__display_card(second_card)
            self.__check_game_win()
            self.save_state()

        else:
            self.__display_card(first_card)
            self.__display_card(second_card)
            print("Invalid move")


    def __is_black_suit(self, card):
        return card.suit == 'Clubs' or card.suit == 'Spades'

    def __is_opposite_colour(self, card_1, card_2):
        red_and_black = self.__is_black_suit(card_1) and not self.__is_black_suit(card_2)
        back_and_red = not self.__is_black_suit(card_1) and self.__is_black_suit(card_2)

        return red_and_black or back_and_red
    
    def __is_one_smaller_value(self, card_1: Card, card_2:Card):
        return card_1.get_value() + 1 == card_2.get_value() 
    
    def __is_valid_move(self, card_1, card_2):
        return self.__is_opposite_colour(card_1, card_2) and  self.__is_one_smaller_value(card_1, card_2)

    def __is_moving_to_empty_foundation(self, card_1: Card, foundation):
        return foundation == None and card_1.rank == 'A'



    def __display_card(self, card):
            print(card.rank, card.suit)

    def save_state(self):
        with open('solitaire_state.pkl', 'wb') as f:
            pickle.dump(self.piles, f)
            pickle.dump(self.foundations, f)


    def load_state(self):
        if os.path.exists('solitaire_state.pkl'):
            with open('solitaire_state.pkl', 'rb') as f:
                self.piles = pickle.load(f)
                self.foundations = pickle.load(f)
        else:
            print("No saved game state found. Please run 'setup_game' first.")


    def display_all_cards(self):
        for index, foundation in enumerate(self.foundations):
            if foundation:
                print('[' + foundation[-1].display() + ']')
            else: print('[] ' + CARD_SUITS[index])
        print('')


        for pile in self.piles:
            display_pile = []
            for card in pile:
                if(card.visible):
                   display_pile.append(card.display()),
                else:
                    display_pile.append('hidden')
            print(display_pile)
            
    
    def move_to_foundation(self, pile_index, foundation_index):
        success = Foundations().move_card(self.foundations, self.piles, pile_index, foundation_index)
        if success:
            self.display_all_cards()
            self.__check_game_win()
            self.save_state()
        
    

def main():
    parser = argparse.ArgumentParser(description="The index of the stack to take from, followed by the index of the stack to move to.")
    parser.add_argument('operation', choices=['deal', 'move_cards', 'see_cards', 'move_to_foundation'], help="The operation to perform.")
    parser.add_argument('num1',nargs='?', type=int, help="The first stack.")
    parser.add_argument('num2',nargs='?', type=int, help="The second stack.")
    
    args = parser.parse_args()

    if args.operation == 'deal':
        game.setup()
        game.display_all_cards()
    if args.operation == 'see_cards':
        game.load_state()
        game.display_all_cards()
    if args.operation == 'move_cards':
        game.load_state()
        game.move_cards(args.num1, args.num2)
    if args.operation == 'move_to_foundation':
        game.load_state()
        game.move_to_foundation(args.num1, args.num2)

   
game = Solitaire()

# Call the main function to handle commands
if __name__ == "__main__":
    main()


        




