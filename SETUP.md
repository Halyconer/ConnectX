# Connect4 Game Setup for Raspberry Pi

This guide will help you set up the Connect4 Flask server on your Raspberry Pi so it can be accessed from your main portfolio website.

## Prerequisites

- Python 3.13+ installed on your Pi
- Poetry installed for dependency management

## Setup Instructions

### 1. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

Navigate to the connectX directory and install dependencies:

```bash
cd /path/to/Welcome-to-my-Portfolio/connectX
poetry install
```

### 3. Update the API URL in your main portfolio

In your main `index.html`, update the `CONNECT4_API_BASE` constant to point to your Pi's IP address:

```javascript
const CONNECT4_API_BASE = 'http://YOUR_PI_IP_ADDRESS:5000'; // Replace with your Pi's actual IP
```

For example:
```javascript
const CONNECT4_API_BASE = 'http://192.168.1.100:5000';
```

### 4. Run the Flask Server

Start the Connect4 game server:

```bash
poetry run python app.py
```

The server will start on `http://0.0.0.0:5000` and will be accessible from other devices on your network.

### 5. Test the Integration

1. Make sure your Pi is connected to the same network as the device accessing your portfolio
2. Open your portfolio website
3. Click on the "Connect 4 AI" project card
4. Click "New Game" to test the connection

## Troubleshooting

### CORS Issues
- The Flask app is configured with CORS enabled to allow cross-origin requests
- Make sure flask-cors is installed (it should be included in the dependencies)

### Connection Issues
- Verify your Pi's IP address with `hostname -I`
- Make sure port 5000 is not blocked by a firewall
- Test the API directly by visiting `http://YOUR_PI_IP:5000/` in a browser

### Network Access
- If accessing from outside your local network, you may need to:
  - Configure port forwarding on your router
  - Use a service like ngrok for temporary external access

## Running as a Service (Optional)

To keep the game server running automatically, you can create a systemd service:

1. Create a service file:
```bash
sudo nano /etc/systemd/system/connect4.service
```

2. Add the following content:
```ini
[Unit]
Description=Connect4 Game Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/path/to/Welcome-to-my-Portfolio/connectX
ExecStart=/home/pi/.local/bin/poetry run python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable connect4.service
sudo systemctl start connect4.service
```

## API Endpoints

The Flask server provides these endpoints:

- `GET /` - Serves the standalone game interface
- `POST /play` - Start a new game
- `GET /game_state` - Get current game state
- `POST /move` - Make a move (expects JSON with "column" field)

The main portfolio integrates with `/play` and `/move` endpoints to provide the game functionality.
