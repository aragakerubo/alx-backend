// 4. Node Redis client and advanced operations

// In a file named 4-redis_advanced_op.js, let’s use the client to store a hash value

// Create Hash:
// Using hset, let’s store the following:

// The key of the hash should be HolbertonSchools
// It should have a value for:
// Portland=50
// Seattle=80
// New York=20
// Bogota=20
// Cali=40
// Paris=2
// Make sure you use redis.print for each hset
// Display Hash:
// Using hgetall, display the object stored in Redis. It should return the following:

// Requirements:

// Use callbacks for any of the operation, we will look at async operations later

import redis from "redis";

const client = redis.createClient();
client.on("error", (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
});
client.on("connect", () => {
    console.log("Redis client connected to the server");
});

const hashKey = "HolbertonSchools";
const hashValue = {
    Portland: 50,
    Seattle: 80,
    "New York": 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
};

for (const key in hashValue) {
    client.hset(hashKey, key, hashValue[key], redis.print);
}

client.hgetall(hashKey, (error, object) => {
    if (error) throw error;
    else console.log(object);
});
