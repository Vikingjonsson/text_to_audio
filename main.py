import os

from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from text_to_audio.text_to_audio import list_elevenlabs_voices, save_text_as_audio_file

load_dotenv()


def main():
    api_key = os.getenv("elevenlabs_api_key")
    if not api_key:
        print("Error: elevenlabs_api_key not found in .env file")
        return

    voices = list_elevenlabs_voices(api_key)
    if not voices:
        print("Error: No voices found.")
        return

    voice_choices = [Choice(voice.name) for voice in voices]

    voice_name = inquirer.select(
        message="Select a voice:",
        choices=voice_choices,
        default=voice_choices[0],
    ).execute()

    if not voice_name:
        print("No voice selected. Exiting.")
        return

    try:
        print(f"\n=== Saving to File with {voice_name} ===")
        output_path = "audio/test_audio.mp3"
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        text = f"Hello, my name is {voice_name}, and this is a test of Eleven Labs text to speech feature."
        success = save_text_as_audio_file(
            api_key, text, output_path, voice_name=voice_name
        )
        if success:
            print("✅ Audio file saved successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
