import smtplib, os, json, logging
from email.message import EmailMessage
from email.mime.text import MIMEText

def notification(message):
    try:
        logging.info("Logging is working in email sender!")
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("MAIL163_ADDRESS")
        sender_password = os.environ.get("MAIL163_PASSWORD")
        reciever_address = message["username"]
        body = f"mp3 file_id: {mp3_fid} is now ready!"

        # Create the email
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = reciever_address
        logging.info("Loaded sending details success!")

        with smtplib.SMTP_SSL('smtp.163.com', 465) as smtp_server:
            smtp_server.set_debuglevel(1)
            smtp_server.login(sender_address, sender_password)
            smtp_server.send_message(msg)
    except Exception as e:
        print(f"Mail failed to send:{e}")
        return e