import unittest
from unittest.mock import Mock, mock_open, patch

from text_to_audio.text_to_audio import (
    get_voice_id_by_name,
    list_elevenlabs_voices,
    save_text_as_audio_file,
    select_voice,
)


class TestTextToAudio(unittest.TestCase):
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

    def test_get_voice_id_by_name_found(self):
        """Test getting voice ID when voice exists."""
        mock_client = Mock()
        mock_voice = Mock()
        mock_voice.name = "Rachel"
        mock_voice.voice_id = "voice_123"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response

        result = get_voice_id_by_name(mock_client, "Rachel")

        self.assertEqual(result, "voice_123")

    def test_get_voice_id_by_name_case_insensitive(self):
        """Test that voice name matching is case insensitive."""
        mock_client = Mock()
        mock_voice = Mock()
        mock_voice.name = "Rachel"
        mock_voice.voice_id = "voice_123"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response

        result = get_voice_id_by_name(mock_client, "RACHEL")

        self.assertEqual(result, "voice_123")

    def test_get_voice_id_by_name_not_found(self):
        """Test getting voice ID when voice doesn't exist."""
        mock_client = Mock()
        mock_voice = Mock()
        mock_voice.name = "Different Voice"
        mock_voice.voice_id = "voice_456"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response

        result = get_voice_id_by_name(mock_client, "Rachel")

        self.assertIsNone(result)

    def test_get_voice_id_by_name_none_name(self):
        """Test handling of voice with None name."""
        mock_client = Mock()
        mock_voice = Mock()
        mock_voice.name = None
        mock_voice.voice_id = "voice_123"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response

        result = get_voice_id_by_name(mock_client, "Rachel")

        self.assertIsNone(result)

    @patch("text_to_audio.text_to_audio.ElevenLabs")
    def test_list_elevenlabs_voices_success(self, mock_elevenlabs_class):
        """Test listing Eleven Labs voices successfully."""
        mock_client = Mock()
        mock_elevenlabs_class.return_value = mock_client

        mock_voice1 = Mock()
        mock_voice1.name = "Rachel"
        mock_voice1.voice_id = "voice_123"
        mock_voice1.category = "premade"

        mock_voice2 = Mock()
        mock_voice2.name = "Liam"
        mock_voice2.voice_id = "voice_456"
        mock_voice2.category = "premade"

        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice1, mock_voice2]
        mock_client.voices.get_all.return_value = mock_voices_response

        result = list_elevenlabs_voices(api_key="test_api_key")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Rachel")
        self.assertEqual(result[1].name, "Liam")

    def test_list_elevenlabs_voices_no_api_key(self):
        """Test listing voices with no API key."""
        result = list_elevenlabs_voices(api_key=None)
        self.assertEqual(result, [])

        result = list_elevenlabs_voices(api_key="")
        self.assertEqual(result, [])

    @patch("text_to_audio.text_to_audio.list_elevenlabs_voices")
    def test_select_voice_no_voices(self, mock_elevenlabs_voices):
        """Test selecting voice when no voices are available."""
        mock_elevenlabs_voices.return_value = []
        result = select_voice(api_key="test_api_key")
        self.assertEqual(result, "Rachel")

    @patch("text_to_audio.text_to_audio.list_elevenlabs_voices")
    @patch("builtins.print")
    def test_select_voice_with_voices(self, mock_print, mock_elevenlabs_voices):
        """Test selecting voice when voices are available."""

        mock_voice1 = Mock()
        mock_voice1.configure_mock(
            name="Rachel",
            voice_id="voice_123",
            category="premade",
            description="Female voice",
        )

        mock_voice2 = Mock()
        mock_voice2.configure_mock(
            name="Liam",
            voice_id="voice_456",
            category="premade",
            description="Male voice",
        )

        mock_elevenlabs_voices.return_value = [mock_voice1, mock_voice2]

        with patch("builtins.input", return_value="1"):
            result = select_voice(api_key="test_api_key")
            self.assertEqual(result, "Rachel")

        with patch("builtins.input", return_value="2"):
            result = select_voice(api_key="test_api_key")
            self.assertEqual(result, "Liam")

        with patch("builtins.input", return_value=""):
            result = select_voice(api_key="test_api_key")
            self.assertEqual(result, "Rachel")

    @patch("text_to_audio.text_to_audio.list_elevenlabs_voices")
    @patch("builtins.print")
    def test_select_voice_invalid_input_then_valid(
        self, mock_print, mock_elevenlabs_voices
    ):
        """Test handling invalid input followed by valid input."""
        mock_voice = Mock()
        mock_voice.configure_mock(
            name="Rachel", voice_id="voice_123", category="premade"
        )
        mock_elevenlabs_voices.return_value = [mock_voice]

        with patch("builtins.input", side_effect=["5", "1"]):
            result = select_voice(api_key="test_api_key")
            self.assertEqual(result, "Rachel")

        with patch("builtins.input", side_effect=["abc", "1"]):
            result = select_voice(api_key="test_api_key")
            self.assertEqual(result, "Rachel")

    @patch("text_to_audio.text_to_audio.list_elevenlabs_voices")
    @patch("builtins.print")
    def test_select_voice_keyboard_interrupt(self, mock_print, mock_elevenlabs_voices):
        """Test handling keyboard interrupt (Ctrl+C)."""
        mock_voice = Mock()
        mock_voice.configure_mock(
            name="Rachel", voice_id="voice_123", category="premade"
        )
        mock_elevenlabs_voices.return_value = [mock_voice]

        with patch("builtins.input", side_effect=KeyboardInterrupt):
            result = select_voice(api_key="test_api_key")
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
