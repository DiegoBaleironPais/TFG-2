import time
from random import randint

from definitions import ORDERED_SHUFFLE

# Variable that contains if the photosensor has detected something
photosensor_shuffler = False
photosensor_dispenser = False
inserted_card = False

# Callback function to receive a notification when the photosensor detects something
def photosensor_shuffler_callback(data):
    
    if data[2] == 0:
        
        # Indicate that the photosensor has detected something
        global photosensor_shuffler
        photosensor_shuffler = True

        # Show some information about the detection
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[3]))
        print(f"{date}: Photosensor detected something.")


class Storage:
    '''
    Object that acts as a card storage, deals cards and plays them.

    Parameters
    ----------
    controller : telemetrix.Telemetrix
        Variable used to access Telemetrix's API methods.
    main_motor : motor.Motor
        Motor attached to the storage.
    photoShuf_pin : int
        Number of the pin that the storage photosensor is connected to.
    photoDispen_pin : int
        Number of the pin that the dispenser photosensor is connected to.
    deck : list
        The cards that the deck has.
    shuffle_type : int
        The type of shuffle.
    extractor_step : int
        The step in which the extractor's ramp is located.
    card_identifier : card_identifier.CardIdentifier
        Card identification system.

    Attributes
    ----------
    controller : telemetrix.Telemetrix
        Variable used to access Telemetrix's API methods.
    main_motor : motor.Motor
        Motor attached to the storage.
    photoShuf_pin : int
        Number of the pin that the storage photosensor is connected to.
    photoDispen_pin : int
        Number of the pin that the dispenser photosensor is connected to.
    deck : list
        The cards that the deck has.
    shuffle_type : int
        The type of shuffle.
    extractor_step : int
        The step in which the extractor's ramp is located.
    num_cards : int
        Card capacity of the storage.
    steps_per_position : int
        Number of motor steps that corresponds to each position
    cards: list
        List containing all of the cards in the storage: The shuffled deck.
    slots : list
        List containing the slot of each card in the storage.
    card_identifier : card_identifier.CardIdentifier
        Card identification system.
    '''

    def __init__(self, controller, main_motor, photoShuf_pin, deck, shuffle_type, extractor_step, card_identifier):
        self.controller = controller
        self.main_motor = main_motor
        self.photoShuf_pin = photoShuf_pin
        self.deck = deck
        self.shuffle_type = shuffle_type
        self.extractor_step = extractor_step
        self.num_cards = len(deck)
        self.steps_per_slot = main_motor.num_steps / self.num_cards
        self.cards = [None] * self.num_cards
        self.slots = [None] * self.num_cards
        self.card_identifier = card_identifier

        controller.set_pin_mode_digital_input(photoShuf_pin, photosensor_shuffler_callback)
        controller.disable_digital_reporting(photoShuf_pin)

    def reset_position(self):
        '''
        Turns the storage to its origin, position 0.
        '''
        # Variable that checks if the storage is in the origin
        global photosensor_shuffler
        photosensor_shuffler = False

        # Enable the photosensor
        self.controller.enable_digital_reporting(self.photoShuf_pin)

        # Turn motor while not in the correct position
        while not photosensor_shuffler:
            self.main_motor.turn(2)
            
        # Once in the correct position, set the storage's position to 0
        self.main_motor.set_current_position(2)

        # Disable the photosensor
        self.controller.disable_digital_reporting(self.photoShuf_pin)

    def insert_next_card(self, card, card_number, position):
        '''
        Inserts a card in a given position of the storage.

        Parameters
        ----------
        card : string
            Card to be inserted.
        card_number : int
            Where the card was in the non-shuffled deck.
        slot_position : int
            Position of the slot in which the next card will be inserted.
        '''
        # Determine the slot of the card

        # Ordered Shuffle
        if self.shuffle_type == ORDERED_SHUFFLE:
            self.slots[position] = position
            slot_position = int(position * self.steps_per_slot)

        # Chaotic Shuffle
        else:
            self.slots[position] = card_number
            slot_position = int(card_number * self.steps_per_slot)

        # Add the card to the current deck in its determined position
        self.cards[position] = card
        
        # Turn the storage to the determined position
        self.main_motor.turn_to(slot_position)

    def shuffle(self):
        '''
        Shuffles the cards and inserts them into the storage.

        Returns
        -------
        positions : list
            Random positions where the cards will go.
        '''
        # Reset current deck
        self.cards = [None] * self.num_cards
        self.slots = [None] * self.num_cards

        # Reset the storage's position
        self.reset_position()
        
        # Obtain which position in the deck is each card going to.
        positions = list(range(self.num_cards))
        
        # To get fully random positions, we use the top-to-random shuffle:
        # - Take the first position and put it in a random place in the list.
        # - Sometimes, that position may be after the last position. Each time a new position
        #   goes after the last one (not the last element of the list), it has the same chance
        #   to be in any position in that subset of slots. For example, when only one position
        #   has gone after the last one and a second one arrives, it has 50% of being before or after that one.
        # - Keep doing this until the last position is the first element of the list.
        # - We end by putting this last position randomly in the list.
        while positions[0] != (self.num_cards - 1):
            positions.insert(randint(0, self.num_cards - 1), positions.pop(0))
        positions.insert(randint(0, self.num_cards - 1), positions.pop(0))

        return positions

    def deal_card(self, card):
        '''
        Extracts the given card from the storage.

        Parameters
        ----------
        card : string
            The card to extract.
        '''
        # Determine in which slot is the card to extract
        card_slot = self.slots[self.cards.index(card)]

        # Obtain in which step is that slot
        card_step = (self.main_motor.current_position - card_slot * self.steps_per_slot) % self.main_motor.num_steps

        # Determine how many steps does the storage need to turn to put the card on the extractor's ramp
        steps_to_extractor = self.extractor_step - card_step

        # Finally, obtain in which step do we need to rotate the storage taking account of the current rotation
        step = self.main_motor.current_position + steps_to_extractor
        
        # Rotate the storage to that step
        self.main_motor.turn_to(int(step))

        # Extract the card by wiggling it forth and back
        self.main_motor.turn(-7)
        self.main_motor.turn(7)