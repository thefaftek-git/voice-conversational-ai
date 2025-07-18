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
