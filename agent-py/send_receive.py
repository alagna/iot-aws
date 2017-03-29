'''
/*
 * Sending and receiving messages to/from AWS
 */
 '''

 # Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

# Configurations
ENDPOINT="adttn6r67dmtu.iot.eu-west-1.amazonaws.com"
ROOT_CA_PATH="/home/pi/projects/iot-aws/agent-py/certificates/root-CA.crt"
PRIVATE_KEY_PATH="/home/pi/projects/iot-aws/agent-py/certificates/rasp-felix001.private.key"
CERTIFICATE_PATH="/home/pi/projects/iot-aws/agent-py/certificates/rasp-felix001.cert.pem"


# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


################
# main method

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("sendReceiveClient")

# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


myMQTTClient.connect()
#myMQTTClient.publish("myTopic", "myPayload", 0)
myMQTTClient.subscribe("myTopic", 1, customCallback)
#myMQTTClient.unsubscribe("myTopic")
#myMQTTClient.disconnect()


# Publish to the same topic in a loop forever
loopCount = 0
while True:
	myMQTTClient.publish("sdk/test/Python", "New Message " + str(loopCount), 1)
	loopCount += 1
	time.sleep(1)
