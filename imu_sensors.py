#
# reading sensors info and printing them
#

from sense_hat import SenseHat
import time
import math

# constants
DIFFERENCE_BETWEEN_GYRO_VALS=.1
DIFFERENCE_BETWEEN_GYRO_VALS_PRINT=.5


# main method
sense = SenseHat()
sense.clear()
sense.set_imu_config(False, True, True)  # gyroscope and accel enabled
print("gyroscope and accelerometer enabled")


old_gyro_raw = sense.get_gyroscope_raw()

while True:
    time.sleep(.1)
    gyro_raw = sense.get_gyroscope_raw()
    # accel_raw = sense.get_accelerometer_raw()
    if (math.fabs(
        (math.fabs(old_gyro_raw['x']) - math.fabs(gyro_raw['x'])))>DIFFERENCE_BETWEEN_GYRO_VALS):
        print("x: {x}, y: {y}, z: {z}".format(**gyro_raw))
    if (math.fabs(
        (math.fabs(old_gyro_raw['x']) - math.fabs(gyro_raw['x'])))>DIFFERENCE_BETWEEN_GYRO_VALS_PRINT):
        sense.show_message("*")
