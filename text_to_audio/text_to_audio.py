from elevenlabs import Voice
from elevenlabs.client import ElevenLabs


def list_elevenlabs_voices(api_key: str | None = None) -> list[Voice]:
    try:

        if not api_key:
            return []

        client = ElevenLabs(api_key=api_key)
        available_voices = client.voices.get_all()

        return available_voices.voices

    except Exception as e:
        print(f"Error fetching Eleven Labs voices: {e}")
        return []


def get_voice_id_by_name(client: ElevenLabs, voice_name: str) -> str | None:
    try:
        available_voices = client.voices.get_all()
        for voice in available_voices.voices:
            if voice.name and voice.name.lower() == voice_name.lower():
                return voice.voice_id
        return None

    except Exception:
        return None


def save_text_as_audio_file(
    api_key: str, text: str, filename: str, voice_name: str = "Rachel"
):
    try:
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