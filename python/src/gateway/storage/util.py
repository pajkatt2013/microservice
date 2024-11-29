import pika, json, logging

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
        logging.info(f"file uploaded to mango,file id:{fid}")
    except Exception as err:
        logging.error(f"File upload failed:{err}")
        return "internal server error", 500
    
    logging.info(f"Access dictionary content: {access}")

    username = access.get("username")
    if not username:
        logging.error("Key 'username' not found in access dictionary.")
        fs.delete(fid)  # Clean up the uploaded file if there's an issue
        logging.info(f"file deleted from mango,file id:{fid}")
        return "username is missing in access data", 400
    
    message = {
        "video_fid": str(fid),
        "mp3_id": None,
        "username": username,
    }

    try:
        channel.basic_publish(
            exchange = '',
            routing_key = 'video',
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        logging.info("succeeded in publishing message in video queue")
    except Exception as err:
        logging.error(f"Failed to publish message in video queue: {err}")
        print(err)
        fs.delete(fid)
        logging.info(f"file deleted from mango,file id:{fid}")
        return "internal server error", 500