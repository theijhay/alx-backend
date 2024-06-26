const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');
const express = require('express');

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

const reserveSeat = (number) => {
    client.set('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return parseInt(seats, 10);
};

let reservationEnabled = true;

// Initialize the number of available seats to 50
reserveSeat(50);

const queue = kue.createQueue();

const app = express();
const port = 1245;

app.use(express.json());

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }

    const job = queue.create('reserve_seat', {}).save((err) => {
        if (!err) {
            res.json({ status: 'Reservation in process' });
        } else {
            res.json({ status: 'Reservation failed' });
        }
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    });
});

app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();
        if (availableSeats <= 0) {
            reservationEnabled = false;
            return done(new Error('Not enough seats available'));
        }

        reserveSeat(availableSeats - 1);

        if (availableSeats - 1 <= 0) {
            reservationEnabled = false;
        }

        done();
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
