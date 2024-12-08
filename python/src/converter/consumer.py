import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3
import logging

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Logging is working in consumer!")
    try:
        uri = (
                "mongodb://mongodb-0.mongodb.default.svc.cluster.local:27017,"
                "mongodb-1.mongodb.default.svc.cluster.local:27017,"
                "mongodb-2.mongodb.default.svc.cluster.local:27017/"
                "?replicaSet=rs0"
            )

        client = MongoClient(uri)
        db_videos = client.videos
        db_mp3s = client.mp3s
        logging.info("succeeded in connecting to mongoclient")
    except Exception as e:
        logging.error(f"An error occurred while connecting to MongoDB: {e}")
    
    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)
    # rabbitmq connection
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = "rabbitmq"))
        channel = connection.channel()
        logging.info("succeeded in connecting to rabbitmq channel")
    except pika.exceptions.AMQPError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")

   
    def callback(ch, method, properties, body):
        logging.info("Received message for processing")
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            logging.error(f"Processing failed: {err}")
            print(f"Processing failed: {err}")
            ch.basic_nack(delivery_tag = method.delivery_tag)
        else:
            logging.info("Processing succeeded, acknowledging message")
            print("Processing succeeded")
            ch.basic_ack(delivery_tag = method.delivery_tag)
            logging.info("acknowledging succeeded")

    channel.basic_consume(
        queue = os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) 
