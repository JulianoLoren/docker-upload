import os
import paramiko
import time
from datetime import datetime

def upload_file():
    try:
        # Get environment variables
        local_path = os.getenv('LOCAL_PATH')
        remote_path = os.getenv('REMOTE_PATH')
        host = os.getenv('REMOTE_HOST')
        port = int(os.getenv('REMOTE_PORT', '22'))
        username = os.getenv('REMOTE_USER')
        password = os.getenv('REMOTE_PASS')
        
        if not all([local_path, remote_path, host, username, password]):
            print("Error: Missing required environment variables")
            return False
            
        # Initialize SSH client
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Upload file
        sftp.put(local_path, remote_path)
        print(f"{datetime.now()}: Successfully uploaded {local_path} to {remote_path}")
        
        # Close connections
        sftp.close()
        transport.close()
        return True
        
    except Exception as e:
        print(f"{datetime.now()}: Error uploading file: {str(e)}")
        return False

def main():
    interval = int(os.getenv('UPLOAD_INTERVAL_MIN', '5')) * 60  # Convert minutes to seconds
    
    print(f"Starting file uploader. Upload interval: {interval//60} minutes")
    
    while True:
        upload_file()
        time.sleep(interval)

if __name__ == "__main__":
    main()
