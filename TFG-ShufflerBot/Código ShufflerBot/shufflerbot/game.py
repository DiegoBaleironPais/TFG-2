
class Game:
    '''
    Parent object that illustrates how a game should be implemented.
    '''

    def __init__(self):
        '''
        Create the Game class.
        '''
        pass

    def setup_game(self):
        '''
        Setups the game (i.e. deals first hand, determines trump...).
        '''
        pass

    def play_next_card(self, player):
        '''
        Plays next player's card.

        Parameters
        ----------
        player : int
            Player who has the current turn.
        '''
        pass

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
        pass

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
        pass

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
        pass
