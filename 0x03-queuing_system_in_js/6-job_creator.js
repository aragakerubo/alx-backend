// 7. Create the Job processor

import kue from "kue";
import redis from "redis";

const message = {
    phoneNumber: "4153518780",
    message: "This is the code to verify your account",
};

const queue = kue.createQueue({
    redis: {
        createClientFactory: () => redis.createClient(),
    },
});

queue.on("job enqueue", function (id, type) {
    console.log(`Notification of job type ${type} with id ${id} is enqueued`);
});

queue.on("job complete", function (id, result) {
    kue.Job.get(id, function (err, job) {
        if (err) return;
        job.remove(function (err) {
            if (err) throw err;
            console.log(
                `Notification of job with id ${job.id} is removed from queue`
            );
        });
    });
});

const job = queue.create("push_notification_code", message).save((err) => {
    if (err) console.log("Notification job failed");
    else console.log(`Notification job created: ${job.id}`);
});
