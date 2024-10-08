// 5. Node Redis client publisher and subscriber

import redis from "redis";

const client = redis.createClient();

client.on("connect", () => {
    console.log("Redis client connected to the server");
});

client.on("error", (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

/**
 * Publish a message after a given time
 * @param {string} message - The message to publish
 * @param {integer} time - The time to wait before publishing the message
 * @return {void}
 */
function publishMessage(message, time) {
    setTimeout(() => {
        console.log(`About to send ${message}`);
        client.publish("holberton school channel", message, (error) => {
            if (error) console.log(error);
        });
    }, time);
}

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
