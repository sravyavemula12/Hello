import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "your_email@example.com"  # Replace with your email
    from_password = "your_password"        # Replace with your email password

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Create server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login Credentials for sending the mail
    server.login(from_email, from_password)

    # Send the message via the server.
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)

    server.quit()

def schedule_email(subject, body, to_email, send_time):
    schedule_time = time.strptime(send_time, "%Y-%m-%d %H:%M:%S")
    schedule_time = time.mktime(schedule_time)

    current_time = time.time()
    delay = schedule_time - current_time

    if delay > 0:
        schedule.enter(delay, 1, send_email, (subject, body, to_email))
    else:
        print("Scheduled time is in the past. Please enter a future time.")

def main():
    print("Email Scheduler")
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    to_email = input("Enter the recipient's email: ")
    send_time = input("Enter the send time (YYYY-MM-DD HH:MM:SS): ")

    schedule_email(subject, body, to_email, send_time)
    print("Email scheduled successfully!")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
