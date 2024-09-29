// 13. Can I have a seat?

import redis from "redis";
import { promisify } from "util";
import express from "express";
import kue from "kue";

const app = express();
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const queue = kue.createQueue();

let reservationEnabled = true;
const port = 1245;

client.on("error", (err) => {
    console.log("Error " + err);
});

client.on("connect", () => {
    console.log("Connected to Redis");
});

const reserveSeat = async (number) => {
    await setAsync("available_seats", number);
};

const getCurrentAvailableSeats = async () => {
    return await getAsync("available_seats");
};

const init = async () => {
    await reserveSeat(50);
};

init();

app.get("/available_seats", async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats });
});

app.get("/reserve_seat", async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }

    const job = queue.create("reserve_seat").save((err) => {
        if (err) {
            return res.json({ status: "Reservation failed" });
        }

        res.json({ status: "Reservation in process" });
    });

    job.on("complete", () => {
        console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on("failed", (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

app.get("/process", async (req, res) => {
    res.json({ status: "Queue processing" });

    queue.process("reserve_seat", async (job, done) => {
        try {
            const availableSeats = await getCurrentAvailableSeats();
            if (availableSeats <= 0) {
                throw new Error("Not enough seats available");
            }

            await setAsync("available_seats", availableSeats - 1);
            if (availableSeats - 1 === 0) {
                reservationEnabled = false;
            }

            done();
        } catch (error) {
            done(error);
        }
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
