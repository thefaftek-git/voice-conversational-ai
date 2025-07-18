#!/usr/bin/env python3
"""
Tests for the live transcription functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unittest.mock import Mock, patch
import pytest
from live_transcription import LiveTranscriber

def test_live_transcriber_initialization():
    """Test that the LiveTranscriber initializes correctly."""
    transcriber = LiveTranscriber(model_size="tiny", device="cpu")
    assert transcriber is not None
    assert transcriber.model_size == "tiny"
    assert transcriber.device == "cpu"
    assert transcriber.recorder is None

def test_live_transcriber_start_stop():
    """Test starting and stopping the transcription service."""
    with patch('RealtimeSTT.RealtimeSTT.audio_recorder.AudioToTextRecorder') as mock_recorder:
        # Mock the recorder class
        mock_instance = Mock()
        mock_recorder.return_value = mock_instance

        transcriber = LiveTranscriber(model_size="tiny", device="cpu")

        # Start transcription
        transcriber.start()

        # Verify recorder was initialized with correct parameters
        mock_recorder.assert_called_once_with(
            model_path=None,
            model_name="tiny",
            device="cpu",
            gpu_device_index=0,
            debug_mode=False,
            vad_filter=True,
            normalize_audio=True,
        )

        # Verify start was called
        mock_instance.start.assert_called_once()

        # Stop transcription
        transcriber.stop()

        # Verify stop was called
        mock_instance.stop.assert_called_once()
        assert transcriber.recorder is None

def test_live_transcriber_get_latest_transcript():
    """Test getting the latest transcript."""
    with patch('RealtimeSTT.RealtimeSTT.audio_recorder.AudioToTextRecorder') as mock_recorder:
        # Mock the recorder class
        mock_instance = Mock()
        mock_recorder.return_value = mock_instance

        transcriber = LiveTranscriber(model_size="tiny", device="cpu")
        transcriber.start()

        # Test when no transcript is available
        mock_instance.get_latest_result.return_value = None
        assert transcriber.get_latest_transcript() is None

        # Test when a transcript is available
        mock_instance.get_latest_result.return_value = {"text": "Hello world"}
        assert transcriber.get_latest_transcript() == "Hello world"

def test_live_transcriber_callback():
    """Test the callback functionality."""
    callback_mock = Mock()
    with patch('RealtimeSTT.RealtimeSTT.audio_recorder.AudioToTextRecorder') as mock_recorder:
        # Mock the recorder class
        mock_instance = Mock()
        mock_recorder.return_value = mock_instance

        transcriber = LiveTranscriber(model_size="tiny", device="cpu", on_transcript=callback_mock)
        transcriber.start()

        # Simulate getting a transcript
        mock_instance.get_latest_result.return_value = {"text": "Test callback"}
        result = transcriber.get_latest_transcript()

        # Verify the callback was called with the correct text
        assert result == "Test callback"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
