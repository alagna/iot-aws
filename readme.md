The directory contains the version of the project presented to the https://aws.amazon.com/it/iot-funambol/

The ![architecture](http://url/to/img.png) presents the different component:
- the request gets publish from the rasp through the ![aws sdk]https://github.com/aws/aws-iot-device-sdk-python to aws iot
- aws-iot has a rule to publish the messages to a lambda function
- the aws-lambda stores the info to a dynamoDb
- the aws-lambda sends the sound to an aws-sqs queue
- the html page has some javascript code that reads the aws-sqs queue and plays the sound.
