import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Create an object containing the job data
const jobData = {
    phoneNumber: '1234567890',
    message: 'This is a test message'
};

// Create a job in the push_notification_code queue
const job = queue.create('push_notification_code', jobData).save((err) => {
    if (err) {
        console.error('Notification job failed');
        return;
    }
    console.log(`Notification job created: ${job.id}`);
});

// Event listener for when the job is completed
job.on('complete', () => {
    console.log('Notification job completed');
});

// Event listener for when the job fails
job.on('failed', () => {
    console.log('Notification job failed');
});
