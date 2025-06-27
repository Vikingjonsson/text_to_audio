import os

from dotenv import load_dotenv
from elevenlabs import Voice
from elevenlabs.client import ElevenLabs

load_dotenv()


def list_elevenlabs_voices() -> list[Voice]:
    """
    List all available Eleven Labs voices.
    :return: List of available voices from Eleven Labs.
    """
    try:
        api_key = os.getenv("elevenlabs_api_key")

        if not api_key:
            return []

        client = ElevenLabs(api_key=api_key)
        available_voices = client.voices.get_all()

        print("Available Eleven Labs voices:")
        for voice in available_voices.voices:
            print(f"- {voice.name} (ID: {voice.voice_id})")
            print(f"  Category: {voice.category}")
            print(f"  Description: {getattr(voice, 'description', 'No description')}")
            print()

        return available_voices.voices

    except Exception as e:
        print(f"Error fetching Eleven Labs voices: {e}")
        return []


def get_voice_id_by_name(client: ElevenLabs, voice_name: str) -> str | None:
    """
    Get the voice ID for a given voice name.
    :param client: ElevenLabs client instance.
    :param voice_name: The name of the voice to find.
    :return: Voice ID if found, None otherwise.
    """
    try:
        available_voices = client.voices.get_all()
        for voice in available_voices.voices:
            if voice.name and voice.name.lower() == voice_name.lower():
                return voice.voice_id
        return None

    except Exception:
        return None


def select_voice() -> str | None:
    """
    Display available voices and let user select one.
    :return: Selected voice name or None if cancelled.
    """
    print("Available Eleven Labs Voices:\n")
    voices = list_elevenlabs_voices()

    if not voices:
        print("❌ No voices available. Using default.")
        return "Rachel"

    print(f"Found {len(voices)} available voices:")
    for i, voice in enumerate(voices, 1):
        print(f"{i}. {voice.name} ({voice.category})")
        if hasattr(voice, "description") and voice.description:
            print(f"Description: {voice.description}")

    while True:
        try:
            choice = input(
                f"\nSelect a voice (1-{len(voices)}) or press Enter for default: "
            ).strip()

            if not choice:
                return voices[0].name if voices else "Rachel"

            choice_num = int(choice)
            if 1 <= choice_num <= len(voices):
                voice_index = choice_num - 1
                selected_voice = voices[voice_index]
                print(f"✅ Selected: {selected_voice.name}")
                return selected_voice.name
            else:
                print(f"❌ Please enter a number between 1 and {len(voices)}")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n⚠️  Cancelled by user")
            return None


def save_text_as_audio_file(text: str, filename: str, voice_name: str = "Rachel"):
    """
    Convert text to audio using Eleven Labs and save as MP3 file without playing.
    :param text: The string to be converted to audio.
    :param filename: The filename to save the audio (e.g., "output.mp3").
    :param voice_name: The name of the Eleven Labs voice to use (default: "Rachel").
    :return: True if successful, False otherwise.
    """
    try:
        api_key = os.getenv("elevenlabs_api_key")
        if not api_key:
            raise ValueError("Eleven Labs API key not found in environment variables")

        client = ElevenLabs(api_key=api_key)
        voice_id = get_voice_id_by_name(client, voice_name)

        if not voice_id:
            available_voices = client.voices.get_all()
            if available_voices.voices:
                voice_id = available_voices.voices[0].voice_id
                print(
                    f"Voice '{voice_name}' not found. Using '{available_voices.voices[0].name}' instead."
                )
            else:
                raise ValueError("No voices available")

        print(f"Generating audio with voice: {voice_name}")
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_monolingual_v1",
        )

        audio_bytes = b"".join(audio)
        with open(filename, "wb") as f:
            f.write(audio_bytes)

        print(f"Audio successfully saved to: {filename}")
        return True

    except Exception as e:
        print(f"Error saving audio file: {e}")
        return False
