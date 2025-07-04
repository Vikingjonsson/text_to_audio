import os

from dotenv import load_dotenv

from text_to_audio.text_to_audio import save_text_as_audio_file, select_voice

load_dotenv()


def main():
    api_key = os.getenv("elevenlabs_api_key")
    text = "Hello, this is a test of the audio playback system with AI voice."

    voice_name = select_voice(api_key)
    if not voice_name:
        print("No voice selected. Exiting.")
        return

    try:
        print(f"\n=== Saving to File with {voice_name} ===")
        output_path = "audio/test_audio.mp3"
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        success = save_text_as_audio_file(
            api_key, text, output_path, voice_name=voice_name
        )
        if success:
            print("✅ Audio file saved successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
