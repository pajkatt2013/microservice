import smtplib, os, json, logging
from email.message import EmailMessage

def notification(message):
    try:
        logging.info("Logging is working in email sender!")
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        reciever_address = message["username"]

        logging.info("Loaded sending details success!")

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = reciever_address
        
        session = smtplib.SMTP("smtp.gmail.com", 587)

        logging.info("opening session success!")

        session.starttls()
        session.login(sender_address, sender_password)

        logging.info("login sender email success!")

        session.send_message(msg, sender_address, reciever_address)
        session.quit()
        print("Mail Sent")
    except Exception as e:
        print(f"Mail failed to send:{e}")
        return e