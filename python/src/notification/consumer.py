import pika, sys, os, time
from send import email
import logging

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Logging is working in consumer!")
    
    # rabbitmq connection
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        channel = connection.channel()
        logging.info("succeeded in connecting to rabbitmq channel")
    except pika.exceptions.AMQPError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")

   
    def callback(ch, method, properties, body):
        logging.info("Received message for email notification")
        err = email.notification(body)
        if err:
            logging.error(f"email notification failed: {err}")
            print(f"email notification failed: {err}")
            ch.basic_nack(delivery_tag = method.delivery_tag)
        else:
            logging.info("email notification succeeded, acknowledging message")
            print("email notification succeeded")
            ch.basic_ack(delivery_tag = method.delivery_tag)
            logging.info("acknowledging succeeded")

    channel.basic_consume(
        queue = os.environ.get("MP3_QUEUE"), on_message_callback=callback
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
