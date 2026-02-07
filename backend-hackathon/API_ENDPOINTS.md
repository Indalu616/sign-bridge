# API Endpoints Summary

## Complete Endpoint List

| Endpoint | Method | Purpose | Service Used |
|----------|--------|---------|--------------|
| `/stt` | POST | Speech → Text | OpenAI Whisper |
| `/tts` | POST | Text → Speech | Coqui TTS |
| `/translate-sign` | POST | Text → Sign Video | GIF/Video Fallback |
| `/dialogue` | POST | End-to-end UX call | Whisper + Coqui |
| `/log` | POST | Log usage | File Storage |
| `/health` | GET | Check server status | - |
| `/config` | GET | Return TTS/STT config | - |

## Endpoint Details

### Core Endpoints

#### 1. POST /stt
**Purpose**: Convert speech audio to text using OpenAI Whisper

**Request**:
- `audio_file` (multipart/form-data): Audio file (.wav, .mp3, .m4a, .ogg, .flac)
- `language` (optional query param): Language code (e.g., 'en', 'ar')

**Response**:
```json
{
  "transcript": "Hello, how can I help you?",
  "confidence": null
}
```

---

#### 2. POST /tts
**Purpose**: Convert text to speech using Coqui TTS

**Request**:
```json
{
  "text": "Welcome to Abu Dhabi Municipality!",
  "language": "en-US"
}
```

**Response**: WAV audio file stream

---

#### 3. POST /translate-sign
**Purpose**: Convert text to sign language video/animation

**Request**:
```json
{
  "text": "Where is the hospital?",
  "language": "ASL"
}
```

**Response**:
```json
{
  "video_url": "https://cdn.example.com/signs/where_is_the_hospital.mp4",
  "text": "Where is the hospital?"
}
```

---

#### 4. POST /dialogue
**Purpose**: Orchestrate end-to-end dialogue interaction

**Request**:
```json
{
  "user_input": "Can I pay my bill?",
  "mode": "speech"
}
```

**Response**:
```json
{
  "reply_text": "Yes, please provide your account number.",
  "reply_audio_base64": "UklGRiQAAABXQVZFZm10..."
}
```

---

### Utility Endpoints

#### 5. POST /log
**Purpose**: Log conversation interactions for analytics

**Request**:
```json
{
  "sign_input": "I need water",
  "translated_text": "I need water",
  "response_speech": "Coming right up!",
  "timestamp": "2024-02-07T16:22:10Z",
  "session_id": "abc123"
}
```

**Response**:
```json
{
  "status": "saved",
  "log_id": "log_12345"
}
```

---

#### 6. GET /health
**Purpose**: Check server health and uptime

**Response**:
```json
{
  "status": "ok",
  "uptime": "20h",
  "version": "1.0.0"
}
```

---

#### 7. GET /config
**Purpose**: Get server configuration and enabled features

**Response**:
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

## Testing the Endpoints

### Using curl

```bash
# Test STT
curl -X POST "http://localhost:8000/stt" \
  -F "audio_file=@test.mp3"

# Test TTS
curl -X POST "http://localhost:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en-US"}' \
  --output speech.wav

# Test Dialogue
curl -X POST "http://localhost:8000/dialogue" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Can I pay my bill?", "mode": "speech"}'

# Test Health
curl http://localhost:8000/health

# Test Config
curl http://localhost:8000/config
```

### Using Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation and testing.

## Mobile App Integration

### Recommended Flow

1. **App Startup**: Call `/config` to verify server availability and features
2. **Health Check**: Periodically call `/health` to ensure server is responsive
3. **Speech Input**: Record audio → POST to `/stt` → Display transcript
4. **Text Output**: User types text → POST to `/tts` → Play audio
5. **Sign Language**: Detected sign → POST to `/translate-sign` → Display video
6. **Logging**: After each interaction → POST to `/log` for analytics

### Example Mobile Integration (Pseudocode)

```javascript
// Check server on app startup
const config = await fetch('http://backend:8000/config');
console.log('Server features:', config.features);

// Speech to text
const formData = new FormData();
formData.append('audio_file', audioBlob);
const sttResult = await fetch('http://backend:8000/stt', {
  method: 'POST',
  body: formData
});
const { transcript } = await sttResult.json();

// Text to speech
const ttsResult = await fetch('http://backend:8000/tts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Hello', language: 'en-US' })
});
const audioBlob = await ttsResult.blob();
playAudio(audioBlob);
```
