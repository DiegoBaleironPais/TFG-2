from tkinter import *
from tkinter import ttk


class ConfigureGameScreen(ttk.Frame):
    '''
    Subwindow that contains the game configuration.

    Parameters
    ----------
    parent : ttk.Frame
        Main window.
    selected_game : string
        The selected game.

    Attributes
    ----------
    players_lb : tk.Listbox
        Listbox with the number of players of the game.
    difficulty_lb : tk.Listbox
        Listbox with the difficulty of the game.
    rounds_lb : tk.Listbox
        Listbox with the number of rounds of the game.
    continue_button : ttk.Button
        
    '''
    def __init__(self, parent, selected_game):
        
        # Instantiate the frame
        ttk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=7)
        self.rowconfigure(3, weight=10)
        
        # Frame title
        ttk.Label(self, text="Configurar partida", font=parent.title_font).grid(column=0, row=0, columnspan=3)
        
        # Configuration
        if selected_game == "Brisca":
            players_setting = ["2 Xogadores", "4 Xogadores"]
            difficulty_setting = ["Fácil", "Difícil"]
            rounds_setting = ["1 Rolda", "3 Roldas"]

        elif selected_game == "Parellas":
            players_setting = ["1 Xogador"]
            difficulty_setting = ["Fácil", "Difícil"]
            rounds_setting = ["1 Rolda", "2 Roldas", "3 Roldas"]
        
        ttk.Label(self, text="Nº Xogadores", font=parent.bold_font).grid(column=0, row=1, sticky='ns')
        self.players_lb = Listbox(self, height=len(players_setting), exportselection=False, font=parent.config_font, listvariable=StringVar(value=players_setting))
        self.players_lb.grid(column=0, row=2, sticky='ew')
        self.players_lb.bind("<<ListboxSelect>>", lambda _: self.check_fields())
        
        ttk.Label(self, text="Dificultade", font=parent.bold_font).grid(column=1, row=1, sticky='ns')
        self.difficulty_lb = Listbox(self, height=len(difficulty_setting), exportselection=False, font=parent.config_font, listvariable=StringVar(value=difficulty_setting))
        self.difficulty_lb.grid(column=1, row=2, sticky='ew')
        self.difficulty_lb.bind("<<ListboxSelect>>", lambda _: self.check_fields())
        
        ttk.Label(self, text="Nº Roldas", font=parent.bold_font).grid(column=2, row=1, sticky='ns')
        self.rounds_lb = Listbox(self, height=len(rounds_setting), exportselection=False, font=parent.config_font, listvariable=StringVar(value=rounds_setting))
        self.rounds_lb.grid(column=2, row=2, sticky='ew')
        self.rounds_lb.bind("<<ListboxSelect>>", lambda _: self.check_fields())

        # Return button
        ttk.Button(self, text="<- Volver", command=lambda: parent.show_select_game_screen()).grid(column=0, row=3, sticky='nesw')

        # Continue
        self.continue_button = ttk.Button(self, text=f"Empezar partida de {selected_game}", state="disabled", command=lambda: parent.show_shuffle_screen(selected_game, self.get_settings()))
        self.continue_button.grid(column=1, row=3, columnspan=2, sticky='nesw')

        # Padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def check_fields(self):
        '''
        Checks if all configuration fields have been selected.
        '''
        if len(self.players_lb.curselection()) == 1 and len(self.difficulty_lb.curselection()) == 1 and len(self.rounds_lb.curselection()) == 1:
            self.continue_button.state(['!disabled'])

    def get_settings(self):
        '''
        Gets all information from the configuration fields.

        Returns
        -------
        settings : list
            A list with the game settings.
        '''
        settings = []

        # Get the number of players
        settings.append(int(self.players_lb.get(self.players_lb.curselection()[0])[0]))

        # Get the difficulty
        settings.append(self.difficulty_lb.curselection()[0])

        # Get the number of rounds
        settings.append(int(self.rounds_lb.get(self.rounds_lb.curselection()[0])[0]))

        # Return the settings
        return settings
