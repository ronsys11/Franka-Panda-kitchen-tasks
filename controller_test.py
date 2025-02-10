import pygame
import time

def main():
    # Initialize pygame
    pygame.init()
    pygame.joystick.init()

    # Check if any joystick is connected
    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Please connect a joystick.")
        return

    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick '{joystick.get_name()}' initialized.")

    print("Press buttons to test. Press Ctrl+C to exit.")

    try:
        while True:
            # Pump the event queue
            pygame.event.pump()

            # Check button states
            for button in range(joystick.get_numbuttons()):
                if joystick.get_button(button):
                    print(f"Button {button} pressed.")

            time.sleep(0.1)  # Small delay to avoid flooding the console
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
