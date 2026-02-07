# Testing the Backend API

## Quick Start

### 1. Start the Backend Server

```bash
# Make sure you're in the backend directory
cd c:\Users\DELL\OneDrive\Desktop\backend-hackathon

# Start the FastAPI server
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### 2. (Optional) Start Coqui TTS Server

For the `/tts` endpoint to work, you need Coqui TTS running:

```bash
# In a separate terminal
pip install TTS
tts-server --port 5002
```

### 3. Open the Test Interface

Simply open `test_interface.html` in your web browser:
- Double-click the file, or
- Right-click → Open with → Your browser

## Testing Each Endpoint

### ✅ Endpoints that work WITHOUT Coqui TTS:

1. **GET /health** - Click "Test Health"
2. **GET /config** - Click "Test Config"
3. **POST /translate-sign** - Enter text and click "Test Text-to-Sign"
4. **POST /log** - Enter text and click "Test Logging"

### ⚠️ Endpoints that REQUIRE additional setup:

5. **POST /stt** - Requires:
   - OpenAI API key (already configured ✅)
   - An audio file to upload
   
6. **POST /tts** - Requires:
   - Coqui TTS server running on port 5002
   
7. **POST /dialogue** - Requires:
   - Coqui TTS server running (for audio response)

## Expected Results

### /health
```json
{
  "status": "ok",
  "uptime": "0h 5m",
  "version": "1.0.0"
}
```

### /config
```json
{
  "whisper_model": "whisper-1",
  "coqui_server_url": "http://localhost:5002",
  "tts_model": "tts_models/en/ljspeech/tacotron2-DDC",
  "api_version": "1.0.0",
  "features": {
    "speech_to_text": true,
    "text_to_speech": true,
    "sign_language": true,
    "conversation_logging": true,
    "dialogue_orchestration": true
  }
}
```

### /translate-sign
```json
{
  "video_url": "https://cdn.example.com/signs/default.mp4",
  "text": "Hello"
}
```

### /log
```json
{
  "status": "saved",
  "log_id": "abc-123-def-456"
}
```

## Troubleshooting

### Server Status Shows "Offline"
- Make sure you ran `uvicorn main:app --reload`
- Check that the server is running on port 8000
- Look for errors in the terminal

### CORS Errors
The backend is already configured to allow requests from `localhost`. If you still see CORS errors, make sure you're opening the HTML file in a browser (not running it from a file:// URL in some browsers).

### /tts Returns Error
This is expected if Coqui TTS server is not running. Start it with:
```bash
tts-server --port 5002
```

### /stt Returns Error
- Make sure you selected an audio file
- Check that your OpenAI API key is valid in `.env`
- Supported formats: .mp3, .wav, .m4a, .ogg, .flac

## Interactive API Documentation

FastAPI also provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These allow you to test endpoints directly from the browser with a nice interface!
