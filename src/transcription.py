
"""
Speech-to-text transcription using Whisper.

This module provides functions to transcribe audio files using the Whisper library.
"""

import whisper

def transcribe_mp3(audio_path: str) -> str:
    """
    Transcribe an MP3 file to text using Whisper.

    Args:
        audio_path (str): Path to the MP3 file to transcribe.

    Returns:
        str: The transcribed text.
    """
    # Initialize Whisper model
    model = whisper.load_model("base")

    # Perform transcription
    result = model.transcribe(audio_path)

    return result["text"]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe MP3 files using Whisper")
    parser.add_argument("audio_file", help="Path to the MP3 file to transcribe")

    args = parser.parse_args()

    transcript = transcribe_mp3(args.audio_file)
    print("Transcription:")
    print(transcript)


