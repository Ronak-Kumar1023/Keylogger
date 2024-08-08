import os
import zipfile
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
FILE_PATH = os.getenv('FILE_PATH', '.')

# Ensure the file path ends with a slash
FILE_PATH = FILE_PATH.rstrip('/') + '/'
decryption_dir = FILE_PATH + "logs_decrypted/"

def decrypt_file(encrypted_file, decrypted_file):
    try:
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        fernet = Fernet(ENCRYPTION_KEY)
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted_data)
        print(f"File {encrypted_file} decrypted successfully.")
    except Exception as e:
        print(f"Error decrypting file {encrypted_file}: {e}")

def extract_zip(zip_file, extract_to):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Files extracted to {extract_to} successfully.")
    except Exception as e:
        print(f"Error extracting zip file {zip_file}: {e}")

if __name__ == "__main__":
    # Ensure the decryption directory exists
    os.makedirs(decryption_dir, exist_ok=True)

    # Find all .safe files in the directory
    safe_files = [f for f in os.listdir(FILE_PATH) if f.endswith(".safe")]

    # Process each .safe file
    for safe_file in safe_files:
        encrypted_log_safe = FILE_PATH + safe_file
        decrypted_log_zip = FILE_PATH + safe_file.replace(".safe", ".zip")

        # Decrypt the .safe file
        decrypt_file(encrypted_log_safe, decrypted_log_zip)

        # Extract the decrypted zip file
        if os.path.exists(decrypted_log_zip):
            extract_zip(decrypted_log_zip, decryption_dir)
            # Delete the decrypted zip file after extraction
            os.remove(decrypted_log_zip)
        else:
            print(f"Error: Decrypted zip file {decrypted_log_zip} not found.")
