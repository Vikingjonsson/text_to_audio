# Text to Audio Converter

A Python application that converts text to audio using the Eleven Labs AI voice synthesis API.

## Features

- AI Voices: Uses Eleven Labs API for natural-sounding speech
- Voice Selection: Voice selection from available Eleven Labs voices
- Audio File Export: Save generated audio as MP3 files

## Prerequisites

- Python 3.8 or higher
- Eleven Labs API key, with Sufficient credits/quota and the following permissions:
   - Text-to-Speech access
   - Voice Library access

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd play_text_as_audio
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your Eleven Labs API key to the `.env` file:
   ```
   elevenlabs_api_key=your_api_key_here
   ```

## Usage

### Interactive Mode

Run the main application for an interactive voice selection experience:

```bash
python main.py
```

This will:
1. Display all available Eleven Labs voices
2. Allow you to select a voice by number or use the default
3. Generate audio with the test text
4. Save the audio file to `audio/test_audio.mp3`

### Programmatic Usage

You can also use the functions directly in your own code:

```python
import os
from dotenv import load_dotenv
from text_to_audio.text_to_audio import save_text_as_audio_file, select_voice

load_dotenv()
api_key = os.getenv("elevenlabs_api_key")

voice_name = select_voice(api_key)

success = save_text_as_audio_file(
    api_key=api_key,
    text="Your text here",
    filename="output.mp3",
    voice_name=voice_name or "Rachel"
)

if success:
    print("Audio file created successfully!")
else:
    print("Failed to create audio file.")
```

## Running Tests

Execute the comprehensive test suite:

```bash
# Run all organized test suites (recommended)
python -m unittest text_to_audio.test_voice_management text_to_audio.test_voice_selection text_to_audio.test_audio_generation -v

# Run specific test categories
python -m unittest text_to_audio.test_voice_management -v      # Voice listing and ID lookup
python -m unittest text_to_audio.test_voice_selection -v       # Interactive voice selection
python -m unittest text_to_audio.test_audio_generation -v      # Audio file creation

# Run legacy monolithic test file (still available)
python -m unittest text_to_audio.test_text_to_audio -v
```

### Test Coverage by Category

**Voice Management Tests** (`test_voice_management.py`):
- ✅ Voice ID lookup (found, not found, case-insensitive)
- ✅ Voice listing with/without API key
- ✅ Handling voices with None names

**Voice Selection Tests** (`test_voice_selection.py`):
- ✅ Interactive voice selection interface
- ✅ Invalid input handling and validation
- ✅ Default selection behavior
- ✅ Keyboard interrupt (Ctrl+C) handling

**Audio Generation Tests** (`test_audio_generation.py`):
- ✅ Successful audio file generation
- ✅ API key validation
- ✅ Voice fallback mechanisms

## Project Structure

```
play_text_as_audio/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── README.md               # This file
├── audio/                  # Generated audio files (auto-created)
└── text_to_audio/         # Main package
    ├── __init__.py
    ├── text_to_audio.py   # Core text-to-speech functionality
    ├── test_text_to_audio.py      # Legacy monolithic tests
    ├── test_voice_management.py   # Voice management tests
    ├── test_voice_selection.py    # Voice selection tests
    └── test_audio_generation.py   # Audio generation tests
```

## Available Functions

- **`list_elevenlabs_voices(api_key)`**: Get all available voices from Eleven Labs
- **`get_voice_id_by_name(client, voice_name)`**: Find voice ID by name
- **`select_voice(api_key)`**: Interactive voice selection interface
- **`save_text_as_audio_file(api_key, text, filename, voice_name)`**: Convert text to audio and save as MP3

## Troubleshooting

### Common Issues

1. **"No module named 'dotenv'"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Eleven Labs API key not found"**
   - Ensure your `.env` file exists and contains `elevenlabs_api_key=your_key`
   - Check that the `.env` file is in the project root directory

3. **"No voices available"** or **"Permission denied"**
   - Verify your API key is valid and has the correct permissions:
     - Text-to-Speech access
     - Voice Library access
   - Check your Eleven Labs account has available voices
   - Ensure you have sufficient credits/quota remaining
   - Verify your API key hasn't expired
   - Ensure you have internet connectivity

4. **"Insufficient quota" or "Rate limit exceeded"**
   - Check your Eleven Labs account usage and limits
   - Wait before retrying if you've hit rate limits
   - Consider upgrading your plan if you need more quota

5. **Import errors**
   - Make sure you're running from the project root directory
   - Activate your virtual environment: `source venv/bin/activate`

### API Key Setup Guide

To get a properly configured Eleven Labs API key:

1. **Sign up** at [elevenlabs.io](https://elevenlabs.io)
2. **Navigate** to your profile settings
3. **Generate** a new API key
4. **Ensure** the key has these permissions:
   - Text-to-Speech API access
   - Voice Library API access
5. **Check** your account has sufficient credits
6. **Copy** the key to your `.env` file

## Dependencies

- `elevenlabs==2.5.0` - Eleven Labs AI voice synthesis
- `python-dotenv==1.0.0` - Environment variable management

All other dependencies (httpx, pydantic, etc.) are automatically installed as transitive dependencies.
