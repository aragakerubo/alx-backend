// 12. In stock?

import express from "express";
import { get } from "http";
import redis from "redis";
import { promisify } from "util";

const app = express();
const client = redis.createClient();

app.listen(1245);
console.log("Server running on port 1245");

client.on("connect", () => {
    console.log("Redis client connected to the server");
});

client.on("error", (error) => {
    console.error(`Redis client not connected to the server: ${error.message}`);
});

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const listProducts = [
    {
        itemId: 1,
        itemName: "Suitcase 250",
        price: 50,
        initialAvailableQuantity: 4,
    },
    {
        itemId: 2,
        itemName: "Suitcase 450",
        price: 100,
        initialAvailableQuantity: 10,
    },
    {
        itemId: 3,
        itemName: "Suitcase 650",
        price: 350,
        initialAvailableQuantity: 2,
    },
    {
        itemId: 4,
        itemName: "Suitcase 1050",
        price: 550,
        initialAvailableQuantity: 5,
    },
];

// Add to Redis
listProducts.forEach(async (product) => {
    await setAsync(`item.${product.itemId}`, product.initialAvailableQuantity);
    console.log(`Product ${product.itemId} added to the stock`);
});

const getItemById = (itemId) => {
    return listProducts.find((product) => product.itemId === itemId);
};

const reserveStockById = async (itemId, stock) => {
    await setAsync(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
    return await getAsync(`item.${itemId}`);
};

app.get("/list_products", (req, res) => {
    res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);

    if (!item) {
        res.json({ status: "Product not found" });
        return;
    }

    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({ ...item, currentQuantity: currentQuantity });
});

app.get("/reserve_product/:itemId", async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);

    if (!item) {
        res.json({ status: "Product not found" });
        return;
    }

    const currentQuantity = await getCurrentReservedStockById(itemId);

    if (currentQuantity >= item.initialAvailableQuantity) {
        res.json({ status: "Not enough stock available", itemId: itemId });
        return;
    }

    reserveStockById(itemId, currentQuantity + 1);
    res.json({ status: "Reservation confirmed", itemId: itemId });
});
