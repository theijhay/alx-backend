import kue from 'kue';

/**
 * Create push notification jobs in the provided Kue queue.
 * @param {Array} jobs - An array of job objects to be added to the queue.
 * @param {Object} queue - The Kue queue object.
 * @throws Will throw an error if jobs is not an array.
 */
function createPushNotificationsJobs(jobs, queue) {
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    jobs.forEach((jobData) => {
        const job = queue.create('push_notification_code_3', jobData)
            .save((err) => {
                if (err) {
                    console.log(`Failed to create job: ${err}`);
                    return;
                }
                console.log(`Notification job created: ${job.id}`);
            });

        job.on('complete', () => {
            console.log(`Notification job ${job.id} completed`);
        }).on('failed', (err) => {
            console.log(`Notification job ${job.id} failed: ${err}`);
        }).on('progress', (progress) => {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });
    });
}

export default createPushNotificationsJobs;
