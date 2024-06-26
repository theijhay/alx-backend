const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

function getItemById(id) {
    return listProducts.find(product => product.id === id);
}

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

app.use(express.json());

app.get('/list_products', (req, res) => {
    res.json(listProducts.map(product => ({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock
    })));
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);
    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = product.stock - reservedStock;

    res.json({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock,
        currentQuantity
    });
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);
    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const reservedStock = await getCurrentReservedStockById(itemId);
    if (reservedStock >= product.stock) {
        return res.json({
            status: 'Not enough stock available',
            itemId: product.id
        });
    }

    reserveStockById(itemId, reservedStock + 1);
    res.json({
        status: 'Reservation confirmed',
        itemId: product.id
    });
});

function reserveStockById(itemId, stock) {
    client.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
    const stock = await getAsync(`item.${itemId}`);
    return parseInt(stock) || 0;
}

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
