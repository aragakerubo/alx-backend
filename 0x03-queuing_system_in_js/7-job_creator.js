// 8. Track progress and errors with Kue: Create the Job creator

import kue from "kue";
import redis from "redis";

const jobs = [
    {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
    },
    {
        phoneNumber: "4153518781",
        message: "This is the code 4562 to verify your account",
    },
    {
        phoneNumber: "4153518743",
        message: "This is the code 4321 to verify your account",
    },
    {
        phoneNumber: "4153538781",
        message: "This is the code 4562 to verify your account",
    },
    {
        phoneNumber: "4153118782",
        message: "This is the code 4321 to verify your account",
    },
    {
        phoneNumber: "4153718781",
        message: "This is the code 4562 to verify your account",
    },
    {
        phoneNumber: "4159518782",
        message: "This is the code 4321 to verify your account",
    },
    {
        phoneNumber: "4158718781",
        message: "This is the code 4562 to verify your account",
    },
    {
        phoneNumber: "4153818782",
        message: "This is the code 4321 to verify your account",
    },
    {
        phoneNumber: "4154318781",
        message: "This is the code 4562 to verify your account",
    },
    {
        phoneNumber: "4151218782",
        message: "This is the code 4321 to verify your account",
    },
];

const queue = kue.createQueue({
    redis: {
        createClientFactory: () => redis.createClient(),
    },
});

jobs.forEach((job) => {
    const newJob = queue.create("push_notification_code_2", job).save((err) => {
        if (err) console.log(`Notification job ${newJob.id} failed: ${err}`);
        else console.log(`Notification job created: ${newJob.id}`);
    });

    newJob.on("complete", () => {
        console.log(`Notification job ${newJob.id} completed`);
    });

    newJob.on("failed", (errorMessage) => {
        console.log(`Notification job ${newJob.id} failed: ${errorMessage}`);
    });

    newJob.on("progress", (progress) => {
        console.log(`Notification job ${newJob.id} ${progress}% complete`);
    });
});
