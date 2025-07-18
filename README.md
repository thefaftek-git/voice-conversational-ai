
# Voice Conversational AI

This project aims to develop a new voice conversational AI model. The initial implementation includes Python scripts for both static file transcription and real-time live audio transcription using Whisper models.

## Features

- **Static File Transcription**: Speech-to-text transcription using OpenAI's Whisper model
- **Live Audio Transcription**: Real-time speech recognition with advanced features like:
  - Voice Activity Detection (VAD)
  - Wake word detection support
  - Low-latency real-time processing
  - Automatic GPU/CPU detection and fallback
- Support for MP3 audio files and live microphone input

## Getting Started

### Prerequisites

You'll need Python 3.9+ and pip installed on your system.

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

### Live Audio Transcription (Complete Script)

Here's a complete script you can run to test live transcription from your microphone:

```python
#!/usr/bin/env python3
"""
Live transcription demo script.
Run this file directly to test real-time audio transcription.
"""

import time
from src.live_transcription import LiveTranscriber

def handle_transcript(text):
    """Callback function that gets called with each new transcript."""
    print(f"\n🎤 Transcribed: {text}")

def main():
    """Main function for live transcription demo."""

    # Initialize the transcriber - auto-detects GPU/CPU
    transcriber = LiveTranscriber(
        model_size="tiny",  # Options: "tiny", "base", "small", "medium", "large"
        on_transcript=handle_transcript,
        debug_mode=True
    )

    try:
        print("🚀 Starting live transcription...")
        transcriber.start()

        print("\n🎙️  Speak now! (Press Ctrl+C to stop)")
        print("------------------------------------")

        # Keep the main thread alive while processing
        while True:
            latest = transcriber.get_latest_transcript()
            if latest and "latest" not in locals():
                print(f"\n📢 Latest transcript: {latest}")
                latest = None  # Reset to avoid duplicate printing

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n✋ Stopping transcription...")
    finally:
        transcriber.stop()
        print("🛑 Transcription stopped.")

if __name__ == "__main__":
    main()
```

## Project Structure

- `src/`: Main source code directory
  - `transcription.py`: Static file transcription using Whisper
  - `live_transcription.py`: Live audio transcription with RealtimeSTT
- `tests/`: Test files for both transcription modules
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Running the Demo Script

1. Save the live transcription script above to a file (e.g., `demo_live_transcription.py`)
2. Make it executable:
   ```bash
   chmod +x demo_live_transcription.py
   ```
3. Run the script:
   ```bash
   ./demo_live_transcription.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

