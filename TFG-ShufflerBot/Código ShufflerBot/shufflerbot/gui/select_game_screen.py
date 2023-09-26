from tkinter import *
from tkinter import ttk, messagebox


class SelectGameScreen(ttk.Frame):
    '''
    Subwindow that contains the game selection.

    Parameters
    ----------
    parent : ttk.Frame
        Main window.

    Attributes
    ----------
    games : list
        List of possible games.
    selected_game : string
        Current selected game.
    buttons : list
        Buttons that select the games.
    info_button : ttk.Button
        Game information button.
    continue_button : ttk.Button
        Button that proceeds to the game configuration.
    '''
    
    def __init__(self, parent):

        # Instantiate the frame
        ttk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=7)
        self.rowconfigure(2, weight=2)
        
        # Frame title
        ttk.Label(self, text="Escoller un xogo", font=parent.title_font).grid(column=0, row=0, columnspan=3)
        
        # Games
        self.games = ["Brisca", "Parellas", "En progreso..."]
        self.selected_game = None
        
        self.buttons = []
        
        button = ttk.Button(self, text=self.games[0], command=lambda: self.select_game(0))
        button.grid(column=0, row=1, sticky='nesw')
        self.buttons.append(button)
        
        button = ttk.Button(self, text=self.games[1], command=lambda: self.select_game(1))
        button.grid(column=1, row=1, sticky='nesw')
        self.buttons.append(button)
        
        ttk.Button(self, text=self.games[2], state="disabled").grid(column=2, row=1, sticky='nesw')

        # Information button
        self.info_button = ttk.Button(self, text="(i) Información", state="disabled", command=lambda: self.show_game_info())
        self.info_button.grid(column=0, row=2, sticky='nesw')

        # Continue
        self.continue_button = ttk.Button(self, text="Continuar", state="disabled", command=lambda: parent.show_configure_game_screen(self.selected_game))
        self.continue_button.grid(column=1, row=2, columnspan=2, sticky='nesw')

        # Padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def select_game(self, game):
        '''
        Selects the game chosen by the user.

        Parameters
        ----------
        game : int
            The chosen game.
        '''
        # Select game
        if self.selected_game != self.games[game]:
            self.selected_game = self.games[game]

        # Enable the info and continue buttons
        if self.selected_game != None:
            self.info_button.state(['!disabled'])
            self.continue_button.state(['!disabled'])

        # Modify buttons themes
        for i in range(len(self.buttons)):
            if i == game:
                self.buttons[i]['style'] = 'GameSelected.TButton'
            else:
                self.buttons[i]['style'] = 'TButton'

    def show_game_info(self):
        '''
        Displays the game rules of the selected game.
        '''
        if self.selected_game == self.games[0]:
            info = ("--- COMO XOGAR Á BRISCA ---\n"
                    "- O obxectivo é facer máis puntos que os adversarios.\n"
                    "- O máis común son partidas de 2 ou 4 xogadores.\n"
                    "- A orde das cartas, de maior a menor é a seguinte:\n"
                    "As (11 ptos), Tres (10 ptos), Rei (4 ptos), Cabalo (3 Ptos), "
                    "Sota (2 Ptos), Sete, Seis, Cinco, Catro e Dous.\n"
                    "- Ó comezo, repártense tres cartas a cada xogador. "
                    "O primeiro xogador xoga unha carta, e os demais poden xogar "
                    "unha carta calquera, sen obliga de asistir ao pao nin xogar trunfo. "
                    "Gaña a baza a maior carta xogada de trunfo, ou no seu defecto, "
                    "a carta máis alta do pao de saída."
                    )
            
        elif self.selected_game == self.games[1]:
            info = ("--- COMO XOGAR ÁS PARELLAS ---\n"
                    "- O obxectivo é facer parellas.\n"
                    "- É un xogo solitario, dun único xogador.\n"
                    "- Ó comezo, repártense 20 cartas ao xogador. "
                    "Despois, en cada quenda, o robot mostrará unha carta. Así, "
                    "o xogador terá que xogar unha carta que teña a mesma numeración."
                    )

        messagebox.showinfo(message=info)
