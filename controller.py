import numpy as np
import pygame

class XboxToLogitechWrapper:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        
    def get_axis(self, axis_number):
        # Mapping of Logitech F310 axes to Xbox 360 axes
        axis_mapping = {
            0: 0,    # Left stick horizontal (same)
            1: 1,    # Left stick vertical (same)
            2: 3,    # Right stick horizontal (was 2 on F310)
            3: 4,    # Right stick vertical (was 3 on F310)
        }
        
        if axis_number in axis_mapping:
            return self.joystick.get_axis(axis_mapping[axis_number])
        return 0.0
        
    def get_button(self, button_number):
        # Mapping of Logitech F310 buttons to Xbox 360 buttons
        button_mapping = {
            0: 0,    # A button (same)
            1: 1,    # B button (same)
            2: 2,    # X button (same)
            3: 3,    # Y button (same)
            4: 4,    # LB button (same)
            5: 5,    # RB button (same)
            6: 6,    # Back button (same)
            7: 7,    # Start button (same)
            8: 8,    # Left stick press (same)
            9: 9,    # Right stick press (same)
        }
        
        if button_number in button_mapping:
            return self.joystick.get_button(button_mapping[button_number])
        return False

    def has_input(self):
        """Check if there's any active input from the controller"""
        # Check stick movement (with deadzone)
        deadzone = 0.1
        for i in range(self.joystick.get_numaxes()):
            if abs(self.joystick.get_axis(i)) > deadzone:
                return True
                
        # Check buttons
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                return True
                
        return False

class Controller:
    def __init__(self):
        self.gripper_closed = None
        pygame.init()
        pygame.joystick.init()
        self.joystick = XboxToLogitechWrapper()

    def get_action(self):
        # First check if there's any input
        if not self.joystick.has_input():
            return None

        action = np.zeros(9)
        gripper_button_pressed = False

        action[0] = self.joystick.get_axis(0)
        action[1] = self.joystick.get_axis(1)

        action[0] = action[0] * -1
        action[1] = action[1] * -1

        action[2] = self.joystick.get_axis(3)
        action[3] = self.joystick.get_axis(2)
        action[3] = action[3] * -1

        if self.joystick.get_button(0):
            action[4] = -1
        elif self.joystick.get_button(2):
            action[4] = 1
        elif self.joystick.get_button(1):
            self.gripper_closed = True
            gripper_button_pressed = True
        elif self.joystick.get_button(3):
            self.gripper_closed = False
            gripper_button_pressed = True
        elif self.joystick.get_button(4):
            action[5] = 1
        elif self.joystick.get_button(5):
            action[5] = -1
        elif self.joystick.get_button(6):
            action[6] = -1
        elif self.joystick.get_button(7):
            action[6] = 1
        elif self.joystick.get_button(8):
            action[7] = 1
        elif self.joystick.get_button(9):
            action[7] = -1
        #just for deadzone
        mask = np.abs(action) > 0.1
        action = action * mask
        action = np.where(action == -0.0, 0.0, action)

        if np.all(action == 0) and not gripper_button_pressed:
            return None
        else:
            if self.gripper_closed == True:
                action[7] = -1.0
                action[8] = -1.0
            elif self.gripper_closed == False:
                action[7] = 1.0
                action[8] = 1.0
        return action