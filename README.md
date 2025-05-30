# Docker File Uploader

A simple Docker container that periodically uploads a local file to a remote server via SFTP.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Copy the example environment file and update it with your configuration:

   ```bash
   cp .env_sample .env
   ```

2. Edit the `.env` file with your configuration:

   ```env
   TZ=Asia/Ho_Chi_Minh
   LOCAL_PATH=/data/myfile.csv
   REMOTE_PATH=/opt/myfile.csv
   REMOTE_HOST=your-remote-host.com
   REMOTE_PORT=22
   REMOTE_USER=your-username
   REMOTE_PASS=your-password
   UPLOAD_INTERVAL_MIN=5
   ```

## Environment Variables

- `TZ`: Timezone (default: Asia/Ho_Chi_Minh)
- `LOCAL_PATH`: Path to the local file to upload (inside container)
- `REMOTE_PATH`: Path on the remote server to upload to
- `REMOTE_HOST`: Remote server hostname or IP
- `REMOTE_PORT`: Remote server SSH port (default: 22)
- `REMOTE_USER`: Username for SFTP authentication
- `REMOTE_PASS`: Password for SFTP authentication
- `UPLOAD_INTERVAL_MIN`: Interval in minutes between upload attempts

## Usage

### Using Docker Compose (Recommended)

1. Start the container:

   ```bash
   docker-compose up -d
   ```

2. View logs:
   ```bash
   docker-compose logs -f
   ```

3. Stop the container:
   ```bash
   docker-compose down
   ```

### Using Docker Run

You can also run the container directly using `docker run`:

```bash
docker run -d \
  --name file_uploader \
  --restart unless-stopped \
  -v $(pwd)/data:/data \
  -e TZ=Asia/Ho_Chi_Minh \
  -e LOCAL_PATH=/data/myfile.csv \
  -e REMOTE_PATH=/opt/myfile.csv \
  -e REMOTE_HOST=your-remote-host.com \
  -e REMOTE_PORT=22 \
  -e REMOTE_USER=your-username \
  -e REMOTE_PASS=your-password \
  -e UPLOAD_INTERVAL_MIN=5 \
  julianoloren/file-uploader:main
```

Or using environment file:

```bash
echo "TZ=Asia/Ho_Chi_Minh
LOCAL_PATH=/data/myfile.csv
REMOTE_PATH=/opt/myfile.csv
REMOTE_HOST=your-remote-host.com
REMOTE_PORT=22
REMOTE_USER=your-username
REMOTE_PASS=your-password
UPLOAD_INTERVAL_MIN=5" > .env

docker run -d \
  --name file_uploader \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/data:/data \
  julianoloren/file-uploader:main
```

## Volumes

The container mounts the local directory to `/data` inside the container. Make sure your `LOCAL_PATH` in the `.env` file reflects this mapping.

## Security Note

- Never commit the `.env` file to version control
- Consider using SSH keys instead of password authentication for better security
- The `.env` file is included in `.gitignore` by default

## License

This project is open source and available under the [MIT License](LICENSE).
