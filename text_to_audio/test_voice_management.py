import unittest
from unittest.mock import Mock, patch

from text_to_audio.text_to_audio import get_voice_id_by_name, list_elevenlabs_voices


class TestVoiceManagement(unittest.TestCase):
    """Tests for voice listing, selection, and ID lookup functionality."""

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


if __name__ == "__main__":
    unittest.main()
