from tkinter import *
from tkinter import ttk, font

from gui.select_game_screen import SelectGameScreen
from gui.configure_game_screen import ConfigureGameScreen
from gui.shuffle_screen import ShuffleScreen
from gui.game_status_screen import GameStatusScreen

class RobotApp(Tk):
    '''
    Main window of the user interface.

    Attributes
    ----------
    title_font : font.Font
        Font for the titles.
    bold_font : font.Font
        A bold font.
    config_font : font.Font
        Font for the configuration listboxes.
    '''
    
    def __init__(self, storage, *args, **kwargs):

        self.storage = storage

        # As the card recognition isn't 100% accurate, we need this in order to manually adjust its value
        self.confirmed_card = ""

        # Instantiate the main window
        Tk.__init__(self, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Add the title of the window
        self.title("Robot App")

        # Adjust the dimensions
        self.geometry("480x320")
        self.minsize(480, 320)
        self.maxsize(480, 320)
        #self.attributes('-fullscreen', True) # zoomed
        #self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        # Create fonts and styles
        self.title_font = font.Font(size=35, weight="bold")
        self.bold_font = font.Font(weight="bold")
        self.config_font = font.Font(size=15)

        s = ttk.Style()
        s.configure('GameSelected.TButton', font=('helvetica', 10, 'bold', 'underline'), foreground='blue')

        # Instantiate and show the game selection screen
        self.show_select_game_screen()
        
    def start_app(self):
        '''
        Starts the main event loop.
        '''
        self.mainloop()

    def change_current_frame(self, frame):
        '''
        Changes the frame that is being displayed in the main window.

        Parameters
        ----------
        frame : ttk.Frame
            The new frame to display.
        '''
        # Get all the children of the main window    
        frames = self.winfo_children()

        # If there are two frames, we destroy the first one (the previous one)
        if len(frames) == 2:
            current_frame = frames[0]
            current_frame.grid_forget()
            current_frame.destroy()

        # Show desired frame
        frame.grid(column=0, row=0, sticky='nesw')

    def show_select_game_screen(self):
        '''
        Changes the current shown frame to the game selector screen.
        '''
        # Instantiate the game selector frame
        frame = SelectGameScreen(self)

        # Update the shown frame
        self.change_current_frame(frame)
        
    def show_configure_game_screen(self, selected_game):
        '''
        Changes the current shown frame to the game configurator screen.

        Parameters
        ----------
        selected_game : string
            The selected game.
        '''
        # Instantiate the game configurator frame
        frame = ConfigureGameScreen(self, selected_game)

        # Update the shown frame
        self.change_current_frame(frame)

    def show_shuffle_screen(self, selected_game, game_settings):
        '''
        Changes the current shown frame to the game status screen.

        Parameters
        ----------
        selected_game : string
            The selected game.
        game_settings : list
            A list with the game settings.
        '''
        # Instantiate the game status frame
        frame = ShuffleScreen(self, selected_game, game_settings)

        # Update the shown frame
        self.change_current_frame(frame)

    def show_game_status_screen(self, selected_game, game_settings):
        '''
        Changes the current shown frame to the game status screen.

        Parameters
        ----------
        selected_game : string
            The selected game.
        game_settings : list
            A list with the game settings.
        '''
        # Instantiate the game status frame
        frame = GameStatusScreen(self, selected_game, game_settings)

        # Update the shown frame
        self.change_current_frame(frame)

    def confirm_identified_card(self, identified_card):
        '''
        Displays a modal that asks for confirmation for the identified card.

        Parameters
        ----------
        identified_card : string
            The identified card.
        '''
        # Create a toplevel
        top = Toplevel()

        # Show which card was reconized
        ttk.Label(top, text=f"Carta recoñecida: {identified_card}", font=self.bold_font).grid(column=0, row=0, columnspan=2)

        # Number picker
        ttk.Label(top, text="Número", font=self.bold_font).grid(column=0, row=1, sticky='ns')
        numbers = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
        number_lb = Listbox(top, height=len(numbers), exportselection=False, font=self.config_font, listvariable=StringVar(value=numbers))
        try:
            number_lb.select_set(numbers.index(identified_card[:-1]))
        except:
            number_lb.select_set(0)
        number_lb.grid(column=0, row=2, sticky='ew')

        # Suit picker
        ttk.Label(top, text="Pau", font=self.bold_font).grid(column=1, row=1, sticky='ns')
        suits = ["o", "c", "e", "b"]
        suit_lb = Listbox(top, height=len(suits), exportselection=False, font=self.config_font, listvariable=StringVar(value=suits))
        suit_lb.select_set(suits.index(identified_card[-1]))
        suit_lb.grid(column=1, row=2, sticky='ew')

        # Confirm button
        ttk.Button(top, text="Confirmar", command=lambda: self.close_confirmation_modal(f"{number_lb.get(number_lb.curselection())}{suit_lb.get(suit_lb.curselection())}", top)).grid(column=0, row=3, columnspan=2, sticky='nesw')

        # Make it a modal by grabbing user input and waiting for it to be destroyed
        top.grab_set()
        top.wait_window(top)

    def close_confirmation_modal(self, card, top):
        '''
        Closes the confirmation modal after updating the identified card.

        Parameters
        ----------
        card : string
            The identified card.
        top : tkinter.Toplevel
            The confirmation modal.
        '''
        # Update the identified card
        self.confirmed_card = card
        
        # Close the modal
        top.withdraw()
        top.destroy()
