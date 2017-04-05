from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time, datetime, json, math
import getopt
import socket
import atexit
import signal
import threading

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

class SensorData():
	def __init__(self, x, y, z, reset):
		self.x = x
		self.y = y
		self.z = z
		self.time = int(round(time.time() * 1000))
		self.reset = reset

	def asJSON(self):
		return json.dumps(vars(self), sort_keys=True, indent=4)

###### constants
clientId = "am"
privateKeyPath = "certs/mypi.private.key"
certificatePath = "certs/mypi.cert.pem"
rootCAPath="certs/root-CA.crt"
host="data.iot.eu-west-1.amazonaws.com"
CLOCK_SECS = 2


##### MQTT client
# Init AWSIoTMQTTClient
client = None
client = AWSIoTMQTTClient("basicPubSub")
client.configureEndpoint(host, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
client.connect()


### main object

sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)

started = False


def startPublish(value, min_value=0, max_value=7):
	global started
	if not started:
		sense.show_message("*")
		raw = sense.get_accelerometer_raw()
		publish(SensorData(raw["x"], raw["y"], raw["z"], True))
		started = True

def stopPublish(value, min_value=0, max_value=7):
	global started
	if started:
		sense.show_message("bye")
		raw = sense.get_accelerometer_raw()
		publish(SensorData(raw["x"], raw["y"], raw["z"], True))
		started = False


def publish(sensorData):
	jsonData = sensorData.asJSON()
	client.publish("sensordata/%s" % clientId, jsonData, 1)
	print(jsonData)

sense.stick.direction_middle = startPublish
sense.stick.direction_up = stopPublish

# --- main loop ---
print("starting main loop")
while True:
    time.sleep(CLOCK_SECS)

    if started:
    	raw = sense.get_accelerometer_raw()
    	print("x: {x}, y: {y}, z: {z}".format(**raw))
	publish(SensorData(raw["x"], raw["y"], raw["z"], False))

