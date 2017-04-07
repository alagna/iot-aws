'use strict';

const doc = require('dynamodb-doc');
const AWS = require('aws-sdk');

const sqs = new AWS.SQS({region : 'eu-west-1'});
const dynamo = new doc.DynamoDB();

const QUEUE_URL = 'https://sqs.eu-west-1.amazonaws.com/271826041478/sounds';

exports.handler = (event, context, callback) => {
    const reset = event.reset || false;
    let soundEvent;

    function publishSound() {
        const soundParams = {
            MessageBody: JSON.stringify(soundEvent),
            QueueUrl: QUEUE_URL
        };

        sqs.sendMessage(soundParams, function(err,data){
            if (err) {
                console.log('error:',"Fail Send Message" + err);
            } else {
                console.log('data:', data.MessageId);
                callback(); // all done
            }
        });
    }

    if (reset) {
        console.log('RESET!!!');
        return callback();
    }

    console.log('READING PARAMETERS', event.time, event.x, event.y, event.z);

    soundEvent = event;

    publishSound();

    // retrieve the previous data
    // const params = {
    //     TableName : "acceleration",
    //     FilterExpression: "#time < :time",
    //     ExpressionAttributeNames:{
    //         "#time": "time"
    //     },
    //     ExpressionAttributeValues: {
    //         ":time": event.time
    //     }
    // };

    // dynamo.scan(params, function(err, data) {
    //     if (err) {
    //         console.log("Unable to query. Error:", JSON.stringify(err, null, 2));
    //     } else {
    //         const previousData = data.Items.length > 0 ? data.Items.sort((a, b) => b.time - a.time)[0] : {
    //             vy: 0,
    //             sy: 0,
    //             time: (event.time - 100)
    //         };

    //         let deltaTime = (event.time - previousData.time);
    //         var vy = previousData.vy + event.y * deltaTime;
    //         var sy = 0.5 * event.y * Math.pow(deltaTime, 2) + previousData.vy * deltaTime + previousData.sy;

    //         soundEvent = event;

    //         dynamo.putItem({
    //             TableName: 'acceleration',
    //             Item: {
    //                 time: event.time,
    //                 sy: sy,
    //                 vy: vy
    //             }
    //         }, publishSound);
    //     }

    // });
};
