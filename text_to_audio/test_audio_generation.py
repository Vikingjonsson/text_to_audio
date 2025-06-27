import unittest
from unittest.mock import Mock, mock_open, patch

from text_to_audio.text_to_audio import save_text_as_audio_file


class TestAudioGeneration(unittest.TestCase):
    """Tests for audio file generation and saving functionality."""

    @patch("text_to_audio.text_to_audio.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("text_to_audio.text_to_audio.get_voice_id_by_name")
    def test_save_text_as_audio_file_success(
        self,
        mock_get_voice_id,
        mock_file,
        mock_elevenlabs_class,
    ):
        """Test successful audio file saving."""
        mock_client = Mock()
        mock_elevenlabs_class.return_value = mock_client
        mock_get_voice_id.return_value = "voice_123"
        mock_client.text_to_speech.convert.return_value = iter([b"audio_data"])

        result = save_text_as_audio_file(
            api_key="test_api_key",
            text="Hello world!",
            filename="test.mp3",
            voice_name="Rachel",
        )

        self.assertTrue(result)
        mock_elevenlabs_class.assert_called_once_with(api_key="test_api_key")
        mock_get_voice_id.assert_called_once_with(mock_client, "Rachel")
        mock_client.text_to_speech.convert.assert_called_once_with(
            voice_id="voice_123", text="Hello world!", model_id="eleven_monolingual_v1"
        )
        mock_file.assert_called_once_with("test.mp3", "wb")
        mock_file().write.assert_called_once_with(b"audio_data")

    def test_save_text_as_audio_file_no_api_key(self):
        """Test handling of missing API key."""
        result = save_text_as_audio_file(
            api_key="", text="Hello world!", filename="test.mp3"
        )

        self.assertFalse(result)

    @patch("text_to_audio.text_to_audio.ElevenLabs")
    @patch("text_to_audio.text_to_audio.get_voice_id_by_name")
    def test_save_text_as_audio_file_voice_not_found_fallback(
        self, mock_get_voice_id, mock_elevenlabs_class
    ):
        """Test fallback when requested voice is not found."""
        mock_client = Mock()
        mock_elevenlabs_class.return_value = mock_client
        mock_get_voice_id.return_value = None

        mock_voice = Mock()
        mock_voice.voice_id = "fallback_voice_123"
        mock_voice.name = "Default Voice"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response
        mock_client.text_to_speech.convert.return_value = iter([b"fallback_audio"])

        with patch("builtins.open", mock_open()):
            result = save_text_as_audio_file(
                api_key="test_api_key",
                text="Hello world!",
                filename="test.mp3",
                voice_name="NonExistentVoice",
            )

        self.assertTrue(result)
        mock_client.text_to_speech.convert.assert_called_once_with(
            voice_id="fallback_voice_123",
            text="Hello world!",
            model_id="eleven_monolingual_v1",
        )


if __name__ == "__main__":
    unittest.main()
