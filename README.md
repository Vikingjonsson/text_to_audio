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

```bash
python main.py
```
