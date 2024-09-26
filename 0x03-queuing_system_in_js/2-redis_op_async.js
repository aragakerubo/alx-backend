// 3. Node Redis client and async operations

import redis from "redis";
import { promisify } from "util";

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

client.on("connect", () => {
    console.log("Redis client connected to the server");
});

client.on("error", (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, redis.print);
}

// Using promisify, modify the function displaySchoolValue to use ES6 async / await
/**
 * Print the value of a school by name
 * @param {string} schoolName - school name
 * @returns {void}
 */
async function displaySchoolValue(schoolName) {
    try {
        const value = await getAsync(schoolName);
        if (value) console.log(value);
    } catch (error) {
        console.log(error.message);
    }
}

(async () => {
    await displaySchoolValue("Holberton");
    setNewSchool("HolbertonSanFrancisco", "100");
    await displaySchoolValue("HolbertonSanFrancisco");
})();
