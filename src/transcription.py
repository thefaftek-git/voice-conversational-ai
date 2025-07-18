"""
Speech-to-text transcription using Whisper X.

This module provides functions to transcribe audio files using the Whisper X library.
"""

import whisperx

def transcribe_mp3(audio_path: str) -> str:
    """
    Transcribe an MP3 file to text using Whisper X.

    Args:
        audio_path (str): Path to the MP3 file to transcribe.

    Returns:
        str: The transcribed text.
    """
    # Initialize Whisper X model
    model = whisperx.load_model("base")

    # Perform transcription
    result = model.transcribe(audio_path)

    return result["text"]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe MP3 files using Whisper X")
    parser.add_argument("audio_file", help="Path to the MP3 file to transcribe")

    args = parser.parse_args()

    transcript = transcribe_mp3(args.audio_file)
    print("Transcription:")
    print(transcript)
