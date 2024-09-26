// 9. Track progress and errors with Kue: Create the Job processor

import kue from "kue";
import redis from "redis";

const blacklisted = ["4153518780", "4153518781"];

const sendNotification = (phoneNumber, message, job, done) => {
    job.progress(0, 100);
    if (blacklisted.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    } else {
        job.progress(50, 100);
        console.log(
            `Sending notification to ${phoneNumber}, with message: ${message}`
        );
        return done();
    }
};

const queue = kue.createQueue({
    redis: {
        createClientFactory: () => redis.createClient(),
    },
});

queue.process("push_notification_code_2", 2, (job, done) => {
    sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
