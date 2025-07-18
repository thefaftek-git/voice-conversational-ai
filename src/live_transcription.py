#!/usr/bin/env python3
"""
Live transcription module using RealtimeSTT for real-time audio processing.

This module provides functionality to transcribe live audio streams
using the RealtimeSTT library, which offers advanced features like:
- Voice Activity Detection (VAD)
- Wake word detection
- Real-time transcription with low latency

Usage:
    from src.live_transcription import LiveTranscriber

    # Initialize and start transcription
    transcriber = LiveTranscriber()
    transcriber.start()

    # Get the latest transcript
    print(transcriber.get_latest_transcript())

    # Stop when done
    transcriber.stop()
"""

import os
import sys
from typing import Optional, Callable
import logging

# Add RealtimeSTT to Python path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "RealtimeSTT"))

try:
    from RealtimeSTT.RealtimeSTT.audio_recorder import AudioToTextRecorder
except ImportError as e:
    raise ImportError(
        "Could not import RealtimeSTT. Please install it using:\n"
        "pip install git+https://github.com/KoljaB/RealtimeSTT.git"
    ) from e

def _is_cuda_available() -> bool:
    """Check if CUDA is available on the system."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False

class LiveTranscriber:
    """
    A class for real-time audio transcription using RealtimeSTT.

    This class provides a simple interface to start and stop live transcription,
    with callbacks for handling transcribed text.
    """

    def __init__(
        self,
        model_size: str = "tiny",
        device: Optional[str] = None,  # Auto-detect
        gpu_device_index: int = 0,
        on_transcript: Optional[Callable[[str], None]] = None,
        debug_mode: bool = False
    ):
        """
        Initialize the live transcriber.

        Args:
            model_size (str): Size of the Whisper model to use. Options: "tiny", "base", "small", "medium", "large"
            device (Optional[str]): Device to run inference on. Auto-detects if None.
                                   Will try CUDA first, then fall back to CPU.
            gpu_device_index (int): GPU device index if using CUDA
            on_transcript (Callable[[str], None]): Callback function to handle transcribed text
            debug_mode (bool): Enable debug logging
        """
        self.model_size = model_size

        # Auto-detect device if not specified
        if device is None:
            if _is_cuda_available():
                self.device = "cuda"
                logging.info("CUDA available, using GPU for transcription")
            else:
                self.device = "cpu"
                logging.info("CUDA not available, falling back to CPU")

        # If device was explicitly specified, use it
        else:
            self.device = device

        self.gpu_device_index = gpu_device_index
        self.on_transcript = on_transcript
        self.debug_mode = debug_mode

        # Configure logging
        if debug_mode:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.recorder = None
        """AudioToTextRecorder: The RealtimeSTT recorder instance"""

    def start(self) -> None:
        """
        Start the live transcription service.

        This will initialize the AudioToTextRecorder and begin processing audio.
        """
        if self.recorder is not None:
            raise RuntimeError("Transcription already started")

        # Initialize the recorder with default settings
        self.recorder = AudioToTextRecorder(
            model_path=None,  # Auto-download the specified model size
            model_name=self.model_size,
            device=self.device,
            gpu_device_index=self.gpu_device_index,
            debug_mode=self.debug_mode,
            vad_filter=True,  # Enable voice activity detection
            normalize_audio=True,  # Normalize audio levels
        )

        # Start the recorder in a separate thread
        self.recorder.start()

        logging.info(f"Live transcription started with {self.model_size} model on {self.device}")

    def stop(self) -> None:
        """
        Stop the live transcription service.

        This will clean up resources and stop audio processing.
        """
        if self.recorder is not None:
            try:
                self.recorder.stop()
                logging.info("Live transcription stopped")
            except Exception as e:
                logging.error(f"Error stopping transcription: {e}")
            finally:
                self.recorder = None

    def get_latest_transcript(self) -> Optional[str]:
        """
        Get the latest transcribed text.

        Returns:
            Optional[str]: The latest transcript, or None if no transcription available
        """
        if self.recorder is None:
            return None

        try:
            # Get the latest result from the recorder
            result = self.recorder.get_latest_result()
            if result and "text" in result:
                return result["text"]
            return None
        except Exception as e:
            logging.error(f"Error getting transcript: {e}")
            return None

    def set_transcript_callback(self, callback: Callable[[str], None]) -> None:
        """
        Set a callback function to handle transcribed text in real-time.

        Args:
            callback (Callable[[str], None]): Function to call with each new transcript
        """
        self.on_transcript = callback

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        self.stop()

def main():
    """Example usage of the LiveTranscriber class."""

    def handle_transcript(text: str):
        print(f"Transcribed: {text}")

    # Initialize and start transcription (auto-detects CUDA)
    transcriber = LiveTranscriber(
        model_size="tiny",
        on_transcript=handle_transcript,
        debug_mode=True
    )

    try:
        transcriber.start()

        # Keep the main thread alive while processing
        print("Press Ctrl+C to stop...")
        import time
        while True:
            latest = transcriber.get_latest_transcript()
            if latest:
                print(f"Latest transcript: {latest}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping transcription...")
    finally:
        transcriber.stop()

if __name__ == "__main__":
    main()

