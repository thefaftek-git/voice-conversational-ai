
# Voice Conversational AI

This project aims to develop a new voice conversational AI model. The initial implementation includes Python scripts for both static file transcription and real-time live audio transcription using Whisper models.

## Features

- **Static File Transcription**: Speech-to-text transcription using OpenAI's Whisper model
- **Live Audio Transcription**: Real-time speech recognition with advanced features like:
  - Voice Activity Detection (VAD)
  - Wake word detection support
  - Low-latency real-time processing
- Support for MP3 audio files and live microphone input

## Getting Started

### Prerequisites

You'll need Python 3.8+ and pip installed on your system.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/thefaftek-git/voice-conversational-ai.git
cd voice-conversational-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Static File Transcription

To transcribe an MP3 file:

```python
from src.transcription import transcribe_mp3

transcript = transcribe_mp3('path/to/your/audio.mp3')
print(transcript)
```

### Live Audio Transcription

For real-time transcription from a microphone:

```python
from src.live_transcription import LiveTranscriber

def handle_transcript(text):
    print(f"Live transcript: {text}")

# Initialize and start transcription
transcriber = LiveTranscriber(
    model_size="tiny",  # Options: "tiny", "base", "small", "medium", "large"
    device="cpu",      # Use "cuda" for GPU acceleration
    on_transcript=handle_transcript,
    debug_mode=True
)

try:
    transcriber.start()

    print("Speak now... Press Ctrl+C to stop")
    while True:
        time.sleep(1)  # Keep main thread alive

except KeyboardInterrupt:
    print("\nStopping transcription...")
finally:
    transcriber.stop()
```

## Project Structure

- `src/`: Main source code directory
  - `transcription.py`: Static file transcription using Whisper
  - `live_transcription.py`: Live audio transcription with RealtimeSTT
- `tests/`: Test files for both transcription modules
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

