# Microservice

## Part 1: Workflow(from user perspective)

> The overall conversion flow is as following steps:

1. **User upload**: when a user uploads a video to be converted to MP3, that request will first hit our gateway. Our gateway will then store the video in mongodb and then put a message on our rabbitmq queue. Downstream services know that there is video to be processed in mongodb.
2. **Converting**: The video to MP3 converter service will consume messages from the queue. It will then get id of the video from the message,pull the video from mongodb, convert the video to MP3, then store the MP3 on mongodb. then put a new message on the queue to be consumed by the notification service that says that the conversion job is done.
3. **Notification**: The notification service consumes those messages from the queue and sends an e-mail notification to the client informing the client that the MP3 for the video that he or she uploaded is ready for download.
4. **Downloading**: The client Then use a unique ID acquired from the notification plus his or her JWT to make requests to the API gateway to download MP3. And the API gateway will pull the MP3 from mongodb and serve it to the client.

## Part 2: Services(from system design perspective)

> There are 5 micro-services in this architecture: auth service, gateway, converter, rabbitmq, notification.

1. **Auth**: Handles user authentication and generates JWT tokens for secure API access.
2. **Gateway**: Acts as the entry point for all client requests, routing them to appropriate services and managing data storage/retrieval in MongoDB.
3. **Converter**: Processes video-to-MP3 conversion by retrieving videos from MongoDB, performing the conversion, and storing the resulting MP3s back in MongoDB.
4. **RabbitMQ**: Manages message queuing to coordinate workflows between services like conversion and notification.
5. **Notification**: Sends email notifications to clients when the MP3 conversion is complete and ready for download.

## Part 3: Steps to deploy



See the original tutorial that I refered [here](https://youtu.be/hmkF77F9TLw?si=zbVzVs1qiEza6g4v).
