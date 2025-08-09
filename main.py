import argparse
import os

from dotenv import load_dotenv

from text_to_audio.text_to_audio import list_elevenlabs_voices, save_text_as_audio_file

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to audio using Eleven Labs API."
    )
    parser.add_argument(
        "--voice", type=str, help="The name of the voice to use.", default=None
    )
    args = parser.parse_args()

    api_key = os.getenv("elevenlabs_api_key")

    voice_name = args.voice

    if not voice_name:
        list_elevenlabs_voices(api_key)
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
