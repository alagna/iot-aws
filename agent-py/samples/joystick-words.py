from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while True:
    for event in sense.stick.get_events():
        print("The joystick was {} {}".format(event.action, event.direction))
        sense.show_message(event.direction)
