import unittest
from unittest.mock import Mock, patch

from text_to_audio.text_to_audio import select_voice


class TestVoiceSelection(unittest.TestCase):
    """Tests for interactive voice selection functionality."""

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
