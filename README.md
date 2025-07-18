# Voice Conversational AI

This project aims to develop a new voice conversational AI model. The initial implementation includes a Python script that uses Whisper X to convert MP3 files to transcripts.

## Features

- Speech-to-text transcription using Whisper X
- Support for MP3 audio files
- Easy-to-use Python interface

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

### Usage

To transcribe an MP3 file:

```python
from src.transcription import transcribe_mp3

transcript = transcribe_mp3('path/to/your/audio.mp3')
print(transcript)
```

## Project Structure

- `src/`: Main source code directory
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
