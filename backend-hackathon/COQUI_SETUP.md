# Coqui TTS Setup Guide

This guide will help you set up a local Coqui TTS server for the Sign Language Interpreter backend.

## 🎯 What is Coqui TTS?

Coqui TTS is an open-source, high-quality neural text-to-speech engine that runs locally without requiring cloud APIs.

## 📦 Installation

### Option 1: Using pip (Recommended)

```bash
pip install TTS
```

### Option 2: Using Docker

```bash
docker pull ghcr.io/coqui-ai/tts
```

## 🚀 Running the TTS Server

### Using pip installation:

```bash
# Start the TTS server on port 5002
tts-server --port 5002
```

### Using Docker:

```bash
docker run -it -p 5002:5002 ghcr.io/coqui-ai/tts --port 5002
```

## 🔧 Configuration

The backend expects the Coqui TTS server to be running at `http://localhost:5002` by default.

You can change this in your `.env` file:

```env
COQUI_SERVER_URL=http://localhost:5002
```

## 🎤 Available Models

Coqui TTS comes with several pre-trained models. To list available models:

```bash
tts --list_models
```

### Recommended Models:

- **English**: `tts_models/en/ljspeech/tacotron2-DDC`
- **Multi-lingual**: `tts_models/multilingual/multi-dataset/your_tts`
- **Fast**: `tts_models/en/ljspeech/fast_pitch`

### Using a specific model:

```bash
tts-server --model_name tts_models/en/ljspeech/tacotron2-DDC --port 5002
```

## 🧪 Testing the Server

Once the server is running, test it with curl:

```bash
curl -X POST http://localhost:5002/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test"}' \
  --output test.wav
```

Or visit the web interface at: `http://localhost:5002`

## 🌐 API Endpoints

### POST `/api/tts`
Convert text to speech

**Request:**
```json
{
  "text": "Hello world",
  "speaker_id": "optional",
  "language_id": "optional"
}
```

**Response:** WAV audio file

### GET `/api/tts/info`
Get server information (available models, speakers, etc.)

### GET `/health`
Health check endpoint

## 🐛 Troubleshooting

### Server won't start
- Make sure port 5002 is not already in use
- Try a different port: `tts-server --port 5003`
- Update `COQUI_SERVER_URL` in `.env` accordingly

### Poor audio quality
- Try a different model (see list above)
- Some models are faster but lower quality

### Out of memory
- Use a smaller/faster model
- Reduce batch size if processing multiple requests

## 📚 Resources

- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [Coqui TTS Documentation](https://tts.readthedocs.io/)
- [Model Zoo](https://github.com/coqui-ai/TTS/wiki/Released-Models)

## 🔄 Integration with Backend

Once the Coqui TTS server is running, your FastAPI backend will automatically connect to it when you call the `/text-to-speech` endpoint.

The backend will:
1. Receive text from the mobile app
2. Forward it to the Coqui TTS server
3. Return the generated audio (WAV format) to the mobile app
