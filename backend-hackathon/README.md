# Sign Language Interpreter - Backend API

Backend API for the Sign Language Interpreter mobile app, providing ML-powered endpoints for speech-to-text, text-to-speech, and sign language output.

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Speech-to-Text**: OpenAI Whisper API
- **Text-to-Speech**: Coqui TTS (self-hosted, local server)
- **Sign Output**: GIF/video-based fallback system
- **Hosting**: Cloud-agnostic (Render, Railway, GCP, etc.)

## 📋 API Endpoints

### Core Endpoints

#### 1. `POST /stt` — Speech-to-Text
Upload audio and get transcribed text using OpenAI Whisper.

**Input**: `multipart/form-data` with `audio_file` (.wav, .mp3, .m4a, .ogg, .flac)

**Response**:
```json
{
  "transcript": "Hello, how can I help you?"
}
```

#### 2. `POST /tts` — Text-to-Speech
Send text and receive Coqui-generated audio (WAV).

**Input**:
```json
{
  "text": "Welcome to Abu Dhabi Municipality!",
  "language": "en-US"
}
```

**Response**: Audio file stream (`audio/wav`)

#### 3. `POST /translate-sign` — Text to Sign Language
Convert text to sign language video/animation.

**Input**:
```json
{
  "text": "Where is the hospital?"
}
```

**Response**:
```json
{
  "video_url": "https://cdn.example.com/signs/where_is_the_hospital.mp4"
}
```

#### 4. `POST /dialogue` — End-to-End Dialogue Orchestration
Orchestrate complete user interaction with speech/text input and audio/text output.

**Input**:
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

### Utility Endpoints

#### 5. `POST /log` — Log Interaction
Log conversation interactions for analytics and debugging.

**Input**:
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

#### 6. `GET /health` — Health Check
Check server readiness status.

**Response**:
```json
{
  "status": "ok",
  "uptime": "20h",
  "version": "1.0.0"
}
```

#### 7. `GET /config` — Server Configuration
Get server-side configuration and enabled features.

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
    "conversation_logging": true
  }
}
```

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Coqui TTS Server
See [COQUI_SETUP.md](COQUI_SETUP.md) for detailed instructions.

Quick start:
```bash
pip install TTS
tts-server --port 5002
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
COQUI_SERVER_URL=http://localhost:5002
```

### 4. Run the Backend Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation
FastAPI provides automatic interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
backend/
│
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── stt.py             # POST /stt (Whisper)
│   ├── tts.py             # POST /tts (Coqui TTS)
│   ├── sign_output.py     # POST /translate-sign
│   ├── session_log.py     # POST /log
│   ├── dialogue.py        # POST /dialogue
│   └── config.py          # GET /config
├── services/
│   ├── whisper_stt.py     # OpenAI Whisper integration
│   ├── coqui_tts.py       # Coqui TTS client
│   └── signall_sdk.py     # Sign language video fallback
├── models/
│   └── schemas.py         # Pydantic models
├── utils/
│   └── audio_utils.py     # Audio processing utilities
├── requirements.txt
├── .env.example
├── .env
├── COQUI_SETUP.md         # Coqui TTS setup guide
├── API_ENDPOINTS.md       # Complete API reference
└── README.md
```

## 📝 Notes
- MediaPipe hand detection runs **client-side** in the mobile app
- Backend uses **OpenAI Whisper** for speech-to-text (requires API key)
- Backend uses **Coqui TTS** for text-to-speech (self-hosted, runs locally)
- Sign language output uses pre-recorded GIF/video fallback system
- Response times target <2 seconds for real-time conversation

## 🔑 API Keys Required
- **OpenAI API Key**: For Whisper speech-to-text (get from [OpenAI Platform](https://platform.openai.com/))
- **Coqui TTS**: No API key needed, runs locally
