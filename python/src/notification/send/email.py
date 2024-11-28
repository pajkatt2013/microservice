import smtplib, os, json, logging
from email.message import EmailMessage
from email.mime.text import MIMEText

def notification(message):
    try:
        logging.info("Logging is working in email sender!")
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        reciever_address = message["username"]
        body = f"mp3 file_id: {mp3_fid} is now ready!"

        msg = EmailMessage()
        msg = MIMEText(body)
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = reciever_address
        logging.info("Loaded sending details success!")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_address, sender_password)
            smtp_server.sendmail(sender_address, reciever_address, msg.as_string())
    except Exception as e:
        print(f"Mail failed to send:{e}")
        return e