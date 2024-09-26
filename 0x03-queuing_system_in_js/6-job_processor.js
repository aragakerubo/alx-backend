// 7. Create the Job processor

import kue from "kue";
import redis from "redis";

const queue = kue.createQueue({
    redis: {
        createClientFactory: () => redis.createClient(),
    },
});

function sendNotification(phoneNumber, message) {
    console.log(
        `Sending notification to ${phoneNumber}, with message: ${message}`
    );
}

queue.process("push_notification_code", (job, done) => {
    const { phoneNumber, message } = job.data;
    sendNotification(phoneNumber, message);
    done();
});
