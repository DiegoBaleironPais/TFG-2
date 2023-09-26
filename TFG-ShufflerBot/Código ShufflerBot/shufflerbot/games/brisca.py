from random import randint
from copy import deepcopy
import time

from storage import Storage


class Brisca:
    '''
    Object that plays a game of Brisca.

    Parameters
    ----------
    parent : ttk.Frame
        Main window.
    deck : list
        A shuffled deck.
    num_players : int
        Number of players, including the CPU.
    difficulty : int
        CPU difficulty.

    Attributes
    ----------
    deck : list
        A shuffled deck.
    trump : char
        Trump of the game.
    num_players : int
        Number of players, including the CPU.
    players : list
        List of players in the game.
    difficulty : int
        CPU difficulty.
    card_values : dict
        Card values and priorities.
    turns : list
        Play order of the actual hand.
    player_cards : list
        Cards of each player.
    hand_cards : list
        Cards played in the actual hand.
    hand_winner : int
        Winner of the actual hand.
    scores : list
        Score of each player.
    '''
    
    def __init__(self, parent, deck, num_players, difficulty):
        self.parent = parent
        self.deck = deck
        self.num_players = num_players
        self.players = list(range(num_players))
        self.difficulty = difficulty

        # Each card has two attributes: its value and its priority.
        self.card_values = {
            "1": [11, 10],
            "2": [0, 1],
            "3": [10, 9],
            "4": [0, 2],
            "5": [0, 3],
            "6": [0, 4],
            "7": [0, 5],
            "10": [2, 6],
            "11": [3, 7],
            "12": [4, 8],
        }

        self.trump = ""
        self.player_cards = [None] * num_players
        self.hand_cards = []
        self.hand_winner = None
        self.scores = [0] * num_players

        self.setup_game()

    def setup_game(self):
        '''
        Setups the game (i.e. deals first hand, determines trump...).
        '''
        # Determine player order
        initial_player = randint(0, self.num_players - 1)
        self.turns = self.players[initial_player:] + self.players[0:initial_player]

        # Deal first cards
        for p in self.players:
            player_turn = self.turns.index(p)
            self.player_cards[p] = [self.deck[card] for card in (player_turn,
                                                                 player_turn + self.num_players,
                                                                 player_turn + self.num_players * 2)]
            
            # If player is not the robot, deal the cards from the storage
            if p != 0:
                for card in self.player_cards[p]:
                    self.parent.storage.deal_card(card)
                time.sleep(5)

        # Remove dealt cards from the deck
        self.deck = self.deck[self.num_players * 3 :]

        # Pick trump and place it last in the deck
        self.trump = self.deck[0][-1]
        self.deck.insert(len(self.deck), self.deck.pop(0))
        print(f"Trump: {self.deck[-1]}\n")

    def play_next_card(self, player):
        '''
        Plays next player's card.

        Parameters
        ----------
        player : int
            Player who has the current turn.
        '''
        # Robot's turn
        if player == 0:
            print(f"Player {player}'s cards: {self.player_cards[player]}")
            
            # Easy CPU Difficulty - Random
            if self.difficulty == 0:
                
                # We play a random card
                played_card_index = randint(0, len(self.player_cards[0]) - 1)
            
            # Hard CPU Difficulty - Heuristic and Minimax algorithm
            elif self.difficulty == 1:

                # We have to determine which card is the best for the robot
                card_to_play = None

                # If there are more than 20 cards remaining, we use an heuristic
                if len(self.deck) + sum([len(player_cards) for player_cards in self.player_cards]) + len(self.hand_cards) > 14:
                    
                    # If the robot doesn't play last
                    if self.turns[-1] != 0:
                        
                        # We play the lowest non-trump card if it's not greater than a king
                        lowest_priority = float('inf')
                        
                        for card in self.player_cards[0]:
                            card_priority = self.card_values[card[:-1]][1]
                            if card[-1] != self.trump and card_priority < lowest_priority and card_priority <= 8:
                                lowest_priority = card_priority
                                card_to_play = card

                        # If it doesn't have a non-trump card, or it's greater than a king,
                        # we play the lowest trump card.
                        if card_to_play == None:
        
                            lowest_priority = float('inf')
                            
                            for card in self.player_cards[0]:
                                card_priority = self.card_values[card[:-1]][1]
                                if card[-1] == self.trump and card_priority < lowest_priority:
                                    lowest_priority = card_priority
                                    card_to_play = card

                    # If the robot plays last
                    else:

                        highest_value = float('-inf')

                        # Get points in the current hand
                        hand_points = 0
                        for card in self.hand_cards:
                            hand_points += self.card_values[card[:-1]][0]
                        
                        # Determine the gain of playing each card, keeping in mind its cost
                        for card in self.player_cards[0]:
                            
                            # How many points does the hand have
                            points_to_gain = hand_points + self.card_values[card[:-1]][0]

                            # How much does it cost to play the card
                            card_cost = self.card_values[card[:-1]][1]
                            if card[-1] == self.trump:
                                card_cost *= 10

                            # Determine the hand winner
                            self.hand_cards.append(card)
                            self.hand_winner = self.get_hand_winner(self.turns, self.hand_cards)
                            del self.hand_cards[-1]
                            if self.hand_winner != 0:
                                points_to_gain *= -1

                            # Calculate the value of playing the card
                            value = points_to_gain * 9.5 - card_cost * 2
                            print(f"Xogar \"{card}\": Ganar {points_to_gain} puntos con coste {card_cost}. Valor: {value}")

                            # Update highest value
                            if value > highest_value:
                                highest_value = value
                                card_to_play = card

                # If there are 20 or less cards remaining, we use minimax
                else:

                    # Create the root node with the current game state
                    root_node = {
                        'deck': self.deck,
                        'player_cards': self.player_cards,
                        'hand_cards': self.hand_cards,
                        'scores': self.scores,
                        'turns': self.turns
                    }

                    # Get the best card to play with minimax
                    card_to_play = self.minimax(root_node, 40, float('-inf'), float('inf'), 0)[1]

                # Get index of the card to play
                played_card_index = self.player_cards[0].index(card_to_play)
            
        # Human's turn
        else:
            print(f"Player {player}'s cards: {self.player_cards[player]}")
            #played_card_index = int(input("Which card do you want to play?: "))

            # Identify the card
            card = self.parent.storage.card_identifier.identify_card(self.parent.storage.card_identifier.PI_CAM_ID)

            # Check if the card was correctly identified and update it
            #self.parent.confirm_identified_card(card)

            # Get index of the card in the user's hand - should refactor as it is no longer neccesary to ask for indexes
            #played_card_index = self.player_cards[player].index(self.parent.confirmed_card)

            # FOR TESTING, assume that the player played its first card
            played_card_index = 0

        # Update player cards and the board
        played_card = self.player_cards[player][played_card_index]
        print(f"Player {player} plays {played_card}.")
        del self.player_cards[player][played_card_index]
        self.hand_cards.append(played_card)
        print(f"Current played cards: {self.hand_cards}.\n")

        # If it was the robot's turn, 'deal' the card
        if player == 0:
            self.parent.storage.deal_card(played_card)
            time.sleep(5)

    def minimax(self, node, depth, alpha, beta, player):
        '''
        Implementation of the minimax algorithm with alpha-beta pruning.

        Parameters
        ----------
        node : dict
            Contains all the information in a current state of the game.
        depth : int
            Maximum allowed depth of the tree expansion.
        alpha : int
            Alpha parameter of the minimax algorithm.
        beta : int
            Beta parameter of the minimax algorithm.
        player : int
            Player that has the current turn.

        Returns
        -------
        best : int
            The best value in a given node.
        card_to_play : string
            The best card to play in a given node.
        '''
        card_to_play = None

        # If we are in a leaf node, or we reached the depth limit, return
        if depth == 0 or len(node['player_cards'][player]) == 0:
            return node['scores'][0], None

        # If the robot has the current turn, we have to maximize
        if player == 0:
            best = float('-inf')
            
        # If a human has the current turn, we have to minimize
        else:
            best = float('inf')

        # Expand the tree with every possible card to play
        for card in node['player_cards'][player]:

            child_node = deepcopy(node)

            # Play the selected card
            del child_node['player_cards'][player][child_node['player_cards'][player].index(card)]
            child_node['hand_cards'].append(card)

            # If it was the last play of the hand, we have to simulate the next hand
            if len(child_node['hand_cards']) == self.num_players:

                # Determine the hand winner
                hand_winner = self.get_hand_winner(child_node['turns'], child_node['hand_cards'])

                # Add points to the hand winner
                self.add_hand_points(child_node['scores'], child_node['hand_cards'], hand_winner)

                # Setup next hand
                child_node['hand_cards'], child_node['turns'], child_node['deck'] = self.setup_next_hand(child_node['hand_cards'], child_node['turns'], hand_winner, child_node['deck'], child_node['player_cards'])


            # Determine whose turn is in the child node
            try:
                next_player = node['turns'][node['turns'].index(player) + 1]
                
            except IndexError:
                next_player = child_node['turns'][0]

            # Explore the generated child node
            value = self.minimax(child_node, depth - 1, alpha, beta, next_player)[0]
            
            # Update the minimax parameters keeping in mind the type of the current player
            
            # If it's the robot
            if player == 0:
                if value > best:
                    card_to_play = card
                    best = value
                alpha = max(alpha, best)
                
            # If it's a human
            else:
                best = min(best, value)
                beta = min(beta, best)

            # Check for alpha-beta pruning
            if beta <= alpha:
                break

        # Return the values of the current node
        return best, card_to_play

    def get_hand_winner(self, turns, hand_cards):
        '''
        Determines which player won the actual hand.

        Parameters
        ----------
        turns : list
            A list that has the index of the players in the order in which they play.
        hand_cards : list
            A list of the cards that have been played in the current hand.

        Returns
        -------
        winner : int
            The hand winner.
        '''
        # First, we take the initial play as the winner
        winner = turns[0]
        winner_card = hand_cards[0]
        winner_card_suit = winner_card[-1]
        winner_card_rank = winner_card[:-1]

        # Then, we compare it to every other card.
        current_turn = 1
        for card in hand_cards[1:]:
            temp_card_suit = card[-1]
            temp_card_rank = card[:-1]
            
            # If the card is better, we pick it as the hand winner
            if (temp_card_suit == winner_card_suit and self.card_values[temp_card_rank][1] > self.card_values[winner_card_rank][1]
                or temp_card_suit == self.trump and winner_card_suit != self.trump):
                    winner = turns[current_turn]
                    winner_card_suit = temp_card_suit
                    winner_card_rank = temp_card_rank
                    winner_card = card
            current_turn += 1

        # Return the hand winner
        return winner

    def add_hand_points(self, scores, hand_cards, hand_winner):
        '''
        Grant the points to the winner of the actual hand.

        Parameters
        ----------
        scores : list
            A list of each player's scores.
        hand_cards : list
            A list of the cards that have been played in the current hand.
        hand_winner : int
            The winner of the actual hand.
        '''
        for card in hand_cards:
            scores[hand_winner] += self.card_values[card[:-1]][0]

    def setup_next_hand(self, hand_cards, turns, hand_winner, deck, player_cards):
        '''
        Setups the next hand (i.e. deals next cards, clears the previous hand...).

        Parameters
        ----------
        hand_cards : list
            A list of the cards that have been played in the current hand.
        turns : list
            A list that has the index of the players in the order in which they play.
        hand_winner : int
            The winner of the actual hand.
        deck : list
            The shuffled deck.
        player_cards : list
            Cards of each player.

        Returns
        -------
        hand_cards : list
            Removed previous cards from the hand.
        turns : list
            Updated turn list.
        deck : list
            Updated deck without cards that have been dealt.
        '''
        # Clear the previous played cards
        hand_cards = []

        # Determine the play order
        turns = self.players[hand_winner:] + self.players[0:hand_winner]

        # Deal next cards
        if len(deck) > 0:
            for player in self.players:
                card = deck[turns.index(player)]
                player_cards[player].append(card)
                # If player isn't the robot, deal the card
                if player != 0:
                    self.parent.storage.deal_card(card)
                    time.sleep(5)
            deck = deck[self.num_players:]

        return hand_cards, turns, deck
