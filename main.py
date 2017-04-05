from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time, datetime, json, math
import getopt
import socket
import atexit
import signal
import threading

from sense_hat import SenseHat


class SensorData():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.readingTime = datetime.datetime.now().isoformat()

	def asJSON(self):
		return json.dumps(vars(self), sort_keys=True, indent=4)

###### constants
clientId = "am"
privateKeyPath = "certs/mypi.private.key"
certificatePath = "certs/mypi.cert.pem"
rootCAPath="certs/root-CA.crt"
host="data.iot.eu-west-1.amazonaws.com"

sense = SenseHat()
sense.clear()
sense.set_imu_config(True, True, True)

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

# --- main loop ---
while True:
    time.sleep(1)

    raw = sense.get_accelerometer_raw()
    print("x: {x}, y: {y}, z: {z}".format(**raw))

    #orientation = sense.get_orientation_degrees()
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

    jsonData = SensorData(raw["x"], raw["y"], raw["z"]).asJSON()
    print(jsonData)
    client.publish("sensordata/%s" % clientId, jsonData, 1)
