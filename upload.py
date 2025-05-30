import paramiko
import os
import time
import shutil
import tempfile
import uuid

def upload_file_to_server():
    local_path = os.getenv('LOCAL_PATH', 'localfile.txt')
    remote_path = os.getenv('REMOTE_PATH', '/home/remoteuser/uploadedfile.txt')
    hostname = os.getenv('REMOTE_HOST', 'your.remote.host')
    port = int(os.getenv('REMOTE_PORT', '8022'))
    username = os.getenv('REMOTE_USER', 'your_username')
    password = os.getenv('REMOTE_PASS', 'your_password')
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix='upload_temp_')
    temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{os.path.basename(local_path)}")
    
    try:
        # Copy file to temporary location
        print(f"📋 Copying {local_path} to temporary location {temp_file_path}")
        shutil.copy2(local_path, temp_file_path)
        
        # Upload from temporary location
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        sftp = ssh.open_sftp()
        sftp.put(temp_file_path, remote_path)
        print(f"✅ Uploaded {local_path} to {hostname}:{remote_path}")

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Failed to upload file: {e}")
    finally:
        # Clean up temporary file and directory
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            print(f"🧹 Cleaned up temporary files")
        except Exception as cleanup_error:
            print(f"⚠️ Failed to clean up temporary files: {cleanup_error}")

if __name__ == "__main__":
    interval = int(os.getenv('UPLOAD_INTERVAL_MIN', '5')) * 60  # convert to seconds
    while True:
        upload_file_to_server()
        print(f"⏳ Waiting {interval // 60} minutes...")
        time.sleep(interval)
