import time


class Motor:
    '''
    Object that allows to control a stepper motor.

    Parameters
    ----------
    controller : telemetrix.Telemetrix
        Variable used to access Telemetrix's API methods.
    pulse_pin : int
        Number of the pin that the engine pulse is connected to.
    direction_pin : int
        Number of the pin that the engine turn direction is connected to.
    num_steps : int
        Number of steps the motor has to do in order to complete a revolution.
    max_vel : int
        Top speed that the motor can reach in steps per second.
    acceleration : int
        Acceleration applied to the motor in steps per second squared.

    Attributes
    ---------
    _id : int
        'Private' variable that identifies the motor.
    controller : telemetrix.Telemetrix
        Variable used to access Telemetrix's API methods.
    num_steps: int
        Number of steps that the motor has.
    current_position: int
        Step in which the motor is right now.
    motor_running : bool
        Variable that contains if a motor is running or not at the moment.
    '''

    def __init__(self, controller, pulse_pin, direction_pin, num_steps, max_vel, acceleration):
        self._id = controller.set_pin_mode_stepper(pin1=pulse_pin, pin2=direction_pin)
        self.controller = controller
        self.num_steps = num_steps
        self.current_position = 0
        self.motor_running = False
        
        self.set_max_vel(max_vel)
        self.set_acceleration(acceleration)

    def set_current_position(self, current_position):
        '''
        Updates the motor's current position.

        Parameters
        ----------
        current_position : int
            Current step that the motor is in.
        '''
        self.current_position = current_position
        self.controller.stepper_set_current_position(self._id, current_position)

    def set_max_vel(self, max_vel):
        '''
        Updates the motor's maximum velocity.

        Parameters
        ----------
        max_vel : int
            Top speed that the motor can reach in steps per second.

        Throws
        ------
        RuntimeError
            The top speed has to be between 1 and 1000 steps per second.
        '''
        self._max_vel = max_vel
        self.controller.stepper_set_max_speed(self._id, max_vel)

    def set_acceleration(self, acceleration):
        '''
        Updates the motor's acceleration.

        Parameters
        ----------
        acceleration : int
            Acceleration applied to the motor in steps per second squared.

        Throws
        ------
        RuntimeError
            The acceleration has to be between 1 and 1000 steps per second squared.
        '''
        self._acceleration = acceleration
        self.controller.stepper_set_acceleration(self._id, acceleration)

    def update_motor_status(self, motor_data):
        '''
        Updates the motor status when it has finished running.

        Parameters
        ----------
        motor_data : list
            A list with data of the last motor turn.
        '''
        # Update that the motor is not running anymore.
        self.motor_running = False

        # Log some information about the rotation
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(motor_data[2]))
        print(f'{date}: Motor with id {motor_data[1]} finished turning.')

    def turn(self, steps):
        '''
        Turns the motor relative to its current position.

        Parameters
        ----------
        steps : int
            Number of steps to turn counterclockwise (negative steps to turn the other way).
        '''
        # Set the number of steps to turn
        self.controller.stepper_move(self._id, steps)

        # Indicate that the motor is running
        self.motor_running = True

        # Turn the motor the number of steps desired
        #time.sleep(.1)
        self.controller.stepper_run(self._id, completion_callback=lambda motor_data: self.update_motor_status(motor_data))
        
        # Wait for the motor to stop turning
        while self.motor_running:
            time.sleep(.1)

        # Update current position - keep it always in the [0, num_steps) range
        self.current_position = self.current_position + steps
        if self.current_position < 0 or self.current_position >= self.num_steps:
            self.current_position = self.current_position % self.num_steps
            self.controller.stepper_set_current_position(self._id, self.current_position)

    def turn_to(self, destination, clockwise=False):
        '''
        Turns the motor to an absolute position (in the [0, num_steps) range) in a given direction.

        Parameters
        ----------
        destination : int
            Step in which the motor will stop.
        clockwise : boolean
            Direction in which the motor will turn. True means clockwise turning, and False, counterclockwise.
        '''                
        # Determine the number of steps to turn
        steps_to_turn = destination - self.current_position

        # If we use the stepper_move_to method, the motor will always turn in the direction that results in the shortest turn.
        # To force it in a fixed way, we have to add or substract a full rotation and move it relatively.
        if clockwise:
            steps_to_turn %= -self.num_steps
        
        else:
            steps_to_turn %= self.num_steps

        # Turn the motor
        self.turn(steps_to_turn)
