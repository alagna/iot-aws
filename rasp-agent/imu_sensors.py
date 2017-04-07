#
# reading sensors info and printing them
#

from sense_hat import SenseHat
import time
import math

# constants


# main method
sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)  # gyroscope and accel enabled
print("gyroscope and accelerometer enabled")


while True:
    time.sleep(1)
    sense = SenseHat()
    raw = sense.get_accelerometer_raw()
    #print("x: {x}, y: {y}, z: {z}".format(**raw))

    orientation = sense.get_orientation_degrees()
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))






    # if (math.fabs(
        #(math.fabs(old_gyro_raw['x']) - math.fabs(gyro_raw['x'])))>DIFFERENCE_BETWEEN_GYRO_VALS):
    #if (math.fabs(
    #    (math.fabs(old_gyro_raw['x']) - math.fabs(gyro_raw['x'])))>DIFFERENCE_BETWEEN_GYRO_VALS_PRINT):
    #    sense.show_message("*")
