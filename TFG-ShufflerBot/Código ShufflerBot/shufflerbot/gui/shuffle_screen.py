import time
from threading import Thread
from tkinter import *
from tkinter import ttk


class ShuffleScreen(ttk.Frame):
    '''
    Subwindow that contains the shows the user the shuffling process.

    Parameters
    ----------
    parent : ttk.Frame
        Main window.
    selected_game : string
        The selected game.
    game_settings : list
        A list with the game settings.
    
    Attributes
    ----------
    parent : ttk.Frame
        Main window.
    selected_game : string
        The selected game.
    game_settings : list
        A list with the game settings.
    '''
    
    def __init__(self, parent, selected_game, settings):

        self.parent = parent
        self.selected_game = selected_game
        self.settings = settings

        # Instantiate the frame
        ttk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        
        # Frame title
        ttk.Label(self, text="Barallado", font=parent.title_font).grid(column=0, row=0)

        # Shuffle instructions
        ttk.Label(self, text="Prema no botón \"Comezar barallado\" para comezar o proceso.").grid(column=0, row=1)
        
        # Start shuffling
        self.start_shuffle = ttk.Button(self, text="Comezar barallado", command=lambda: self.start_shuffle_process())
        self.start_shuffle.grid(column=0, row=2, sticky='ns')

        # Shuffle progress - Bar
        self.shuffle_progress_b = IntVar()
        self.shuffle_progress_b.set(0)
        ttk.Progressbar(self, variable=self.shuffle_progress_b, maximum=40.01).grid(column=0, row=3, sticky='ew')

        # Shuffle progress - Text
        self.shuffle_progress_t = StringVar()
        self.shuffle_progress_t.set(f"0 / {40} cartas")
        ttk.Label(self, textvariable=self.shuffle_progress_t, font=parent.bold_font).grid(column=0, row=4, sticky='ns')

        # Padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def start_shuffle_process(self):
        '''
        Starts all necessary threads for the shuffling process.
        '''
        # Disable the 'start shuffling' button
        self.start_shuffle.state(['disabled'])

        # Start a thread to start the shuffle process
        self.shuffle()

    def shuffle(self):
        '''
        Handles the shuffling process and starts the game once it's done.
        '''
        # Start the shuffle process by determining positions
        positions = self.parent.storage.shuffle()

        # For each card
        for i in range(self.parent.storage.num_cards):

            # Identify the card
            card = self.parent.storage.card_identifier.identify_card(self.parent.storage.card_identifier.PI_CAM_ID)

            # Check if the card was correctly identified and update it
            self.parent.confirm_identified_card(card)
            print(f"Confirmed card is: {self.parent.confirmed_card}")

            # Update progress bar
            self.shuffle_progress_t.set(f"{i + 1} / {self.parent.storage.num_cards} cartas")
            self.shuffle_progress_b.set(i + 1)
            
            # Insert the card
            self.parent.storage.insert_next_card(self.parent.confirmed_card, i, positions[i])

        # Start the game once the shuffle is done
        self.parent.show_game_status_screen(self.selected_game, self.settings)
