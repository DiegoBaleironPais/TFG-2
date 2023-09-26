from threading import Thread
from tkinter import *
from tkinter import ttk

from games.brisca import Brisca


class GameStatusScreen(ttk.Frame):
    '''
    Subwindow that contains the game status.

    Parameters
    ----------
    parent : ttk.Frame
        Main window.

    Attributes
    ----------
    
    '''
    def __init__(self, parent, selected_game, game_settings):

        # Get selected game's settings
        num_players = game_settings[0]
        difficulty = game_settings[1]
        num_rounds = game_settings[2]

        self.parent=parent
        # Instantiate the frame
        ttk.Frame.__init__(self, parent)
        for p in range(num_players):
            self.columnconfigure(p, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        # Frame title
        ttk.Label(self, text=selected_game, font=parent.title_font).grid(column=0, row=0, columnspan=num_players)

        # Players and their scores
        self.scores = []
        
        ttk.Label(self, text="Robot").grid(column=0, row=1, sticky='ns')
        score = StringVar()
        self.scores.append(score)
        self.scores[0].set(0)
        ttk.Label(self, textvariable=self.scores[0], font=parent.bold_font).grid(column=0, row=2, sticky='n')
        
        for player in range(1, num_players):
            ttk.Label(self, text=f"Xogador {player}").grid(column=player, row=1, sticky='ns')
            score = StringVar()
            self.scores.append(score)
            self.scores[player].set(0)
            ttk.Label(self, textvariable=self.scores[player], font=parent.bold_font).grid(column=player, row=2, sticky='n')

        # Current turn
        self.current_turn = StringVar()
        ttk.Label(self, textvariable=self.current_turn, font=parent.bold_font).grid(column=0, row=3, columnspan=num_players, sticky='ns')

        # Padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # Setup the game
        if selected_game == "Brisca":
            self.game = Brisca(parent, parent.storage.cards, num_players, difficulty)

        # Start the game -- This may cause trouble with the interface
        Thread(target=self.play_game).start()

    def play_game(self):
        '''
        Plays the configured game.
        '''
        # While there are cards in the deck
        while len(self.game.player_cards[0]) > 0:

            # Each player plays one card
            for t in self.game.turns:

                # Show current turn
                if t == 0: turn = "Robot"
                else: turn = f"Xogador {t}"
                self.current_turn.set(f"Quenda do {turn}")

                # Play the card                
                self.game.play_next_card(t)

            # Determine the hand winner
            self.game.hand_winner = self.game.get_hand_winner(self.game.turns, self.game.hand_cards)
            print(f"Player {self.game.hand_winner} wins the hand.")

            # Add points to the hand winner
            self.game.add_hand_points(self.game.scores, self.game.hand_cards, self.game.hand_winner)
            for player in range(self.game.num_players):
                self.scores[player].set(self.game.scores[player])
            print(f"Current score: {self.game.scores}.\n---------------\n")

            # Prepare for next hand
            self.game.hand_cards, self.game.turns, self.game.deck = self.game.setup_next_hand(self.game.hand_cards, self.game.turns, self.game.hand_winner, self.game.deck, self.game.player_cards)

        # Go back to main screen
        time.sleep(5)
        self.parent.show_select_game_screen()
        
