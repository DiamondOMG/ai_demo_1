# AI Voice Assistant Demo

A voice-activated AI assistant system that combines wake word detection, speech-to-text, AI processing, and text-to-speech functionality. This project demonstrates a complete voice interface using modern web technologies and AI services.

## Features

- 🎤 **Wake Word Detection**: Uses Porcupine to detect the wake word "bumblebee"
- 🗣️ **Speech-to-Text**: Browser-based speech recognition in Thai language
- 🤖 **AI Processing**: Streams responses from OpenRouter AI API
- 🔊 **Text-to-Speech**: Web Speech API for natural voice output
- 🌐 **Web Interface**: Modern, responsive web interface
- 🔄 **Real-time Communication**: WebSocket-based real-time messaging

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser STT   │◄──►│  Python Server  │◄──►│  OpenRouter AI  │
│   (index.html)  │    │   (server.py)   │    │   (ai_stream.py)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Wake Word       │
                       │ Detection       │
                       │ (wake_word.py)  │
                       └─────────────────┘
```

### Components

- **ai_stream.py**: Handles streaming AI responses from OpenRouter API
- **server.py**: Main HTTP/WebSocket server serving the web interface
- **wake_word.py**: Continuous wake word detection using Porcupine
- **index.html**: Frontend web interface with STT/TTS functionality

### WebSocket Communication

The system uses WebSocket rooms for efficient inter-component communication:

```
WebSocket Rooms:
├── wakeword_room (wake_word.py ส่ง detected)
├── stt_room (index.html ส่ง transcript)
└── ai_room (ai_stream.py ส่ง response)
```

**Message Flow:**

1. **Wake Word Detection**: `wake_word.py` → `wakeword_room` → `index.html`
2. **Speech Recognition**: `index.html` → `stt_room` → `ai_stream.py`
3. **AI Processing**: `ai_stream.py` → `ai_room` → `index.html`

**Room-based Architecture Benefits:**

- Direct component-to-component communication
- No queue management needed
- Each component subscribes only to relevant events
- More responsive and decoupled system

## Requirements

### System Requirements

- Python 3.8+
- Modern web browser with Web Speech API support
- Microphone access
- Internet connection for AI API calls

### Dependencies

```
certifi==2025.8.3
cffi==2.0.0
charset-normalizer==3.4.3
click==8.1.8
colorama==0.4.6
gTTS==2.5.4
idna==3.10
MouseInfo==0.1.3
numpy==2.3.3
pvporcupine==3.0.5
PyAutoGUI==0.9.54
pycparser==2.23
pydub==0.25.1
PyGetWindow==0.0.9
PyMsgBox==2.0.1
pynput==1.8.1
pyperclip==1.10.0
PyRect==0.2.0
PyScreeze==1.0.1
python-dotenv==1.1.1
pytweening==1.2.0
requests==2.32.5
simpleaudio==1.0.4
six==1.17.0
sounddevice==0.5.2
urllib3==2.5.0
websockets==15.0.1
```

## Installation

1. **Clone or download the project files**

   ```bash
   cd ai_demo_1
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:

   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Get OpenRouter API Key**

   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up for an account
   - Generate an API key
   - Add it to your `.env` file

5. **Set up Porcupine Wake Word**
   - The wake word "bumblebee" is pre-configured
   - Access key is included in the code
   - No additional setup required

## Usage

### Starting the Application

1. **Run the server**

   ```bash
   python server.py
   ```

2. **Access the web interface**

   - The server will automatically open `http://localhost:8000/index.html`
   - Or open it manually in your browser

3. **Using the Voice Assistant**

   a. **Wake Word Activation**

   - Say "bumblebee" to activate the assistant
   - The system will automatically start listening

   b. **Voice Commands**

   - Speak in Thai after activation
   - The system will transcribe your speech
   - AI will process and respond

   c. **Manual Activation**

   - Click the "Start" button to begin listening
   - Click again to stop

### Ports Used

- **HTTP Server**: Port 8000
- **WebSocket**: Port 8001

## Configuration

### Wake Word Settings (wake_word.py)

```python
keywords = ['bumblebee']  # Change wake word
sensitivities = [0.7]     # Adjust sensitivity (0.0-1.0)
```

### AI Model Settings (ai_stream.py)

```python
model = "openai/gpt-oss-20b:free"  # Change AI model
```

### Speech Recognition (index.html)

```javascript
recognition.lang = "th-TH"; // Change language
```

## File Structure

```
ai_demo_1/
├── ai_stream.py      # AI response streaming
├── server.py         # Main server application
├── wake_word.py      # Wake word detection
├── index.html        # Web interface
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Troubleshooting

### Common Issues

1. **Wake word not detected**

   - Check microphone permissions
   - Adjust sensitivity in `wake_word.py`
   - Ensure Porcupine access key is valid

2. **Speech recognition not working**

   - Allow microphone access in browser
   - Check if browser supports Web Speech API
   - Try refreshing the page

3. **AI responses not working**

   - Verify OpenRouter API key in `.env`
   - Check internet connection
   - Ensure API quota is available

4. **WebSocket connection failed**
   - Ensure ports 8000 and 8001 are available
   - Check firewall settings
   - Try refreshing the browser

### Debug Mode

Enable debug logging by modifying the server files to add more print statements or use Python's logging module.

## API Reference

### WebSocket Messages

**From Browser to Server:**

```json
{
  "type": "stt",
  "message": "transcribed text"
}
```

**From Server to Browser:**

```json
{
  "type": "wakeword",
  "status": "detected"
}
```

```json
{
  "type": "output",
  "message": "AI response text"
}
```

## Development

### Adding New Features

1. **New Wake Words**: Add keywords to `wake_word.py`
2. **Different AI Models**: Modify model in `ai_stream.py`
3. **Additional Languages**: Update language settings in `index.html`
4. **Custom UI**: Modify `index.html` styles and functionality

### Testing

- Test wake word detection separately: `python wake_word.py`
- Test AI streaming: `python ai_stream.py`
- Test web interface: Open `index.html` directly

## Security Notes

- API keys are stored in environment variables (recommended)
- Consider using HTTPS in production
- Validate and sanitize all inputs
- The wake word access key is hardcoded (consider moving to env vars)

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to fork, modify, and improve this voice assistant system.

---

**Note**: This is a demonstration project. For production use, consider implementing proper error handling, authentication, and security measures.
