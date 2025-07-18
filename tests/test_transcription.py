"""
Tests for the transcription module.
"""

import pytest
from src.transcription import transcribe_mp3

def test_transcription():
    """Test that transcription returns a non-empty string."""
    # Create a simple test MP3 file (this would need to be replaced with an actual test file)
    test_audio = "tests/test_audio.mp3"

    # For now, we'll just check that the function runs without error
    # In a real test suite, you'd have proper test audio files and expected outputs
    transcript = transcribe_mp3(test_audio)

    assert isinstance(transcript, str)
    assert len(transcript) > 0

if __name__ == "__main__":
    pytest.main([__file__])
