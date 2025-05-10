# Azure OpenAI Text-to-Speech Converter

A simple application to convert text to speech using Azure OpenAI's text-to-speech capabilities.

## Features

- Convert text to natural-sounding speech using Azure OpenAI's TTS service
- Multiple voice options (alloy, echo, fable, onyx, nova, shimmer)
- Save audio output as WAV files
- Simple GUI interface for easy use

## Requirements

- Python 3.7+
- Azure OpenAI API subscription (API key and endpoint)

## Setup

1. Ensure you have Python installed
2. Activate the virtual environment:

   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Azure OpenAI credentials (or enter them directly in the GUI):

   ```bash
   # On macOS/Linux
   export AZURE_OPENAI_API_KEY="your-api-key"
   export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export API_VERSION="2025-01-01-preview"
   
   # On Windows
   set AZURE_OPENAI_API_KEY=your-api-key
   set AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   set API_VERSION=2025-01-01-preview
   ```

## Usage

### GUI Application

Run the GUI application:

```bash
python tts_gui.py
```

Enter your Azure OpenAI credentials, choose a voice, enter text, and click "Convert to Speech".

### Command Line

You can also use the command-line interface:

```bash
python azure_tts.py "This is the text you want to convert to speech" [output_file.wav]
```

## Available Voices

The available voices from OpenAI TTS include:
- alloy: A neutral voice with balanced tone
- echo: A warm and clear voice
- fable: An expressive voice for storytelling
- onyx: A deep and authoritative voice
- nova: A bright and professional voice
- shimmer: A melodic and soft voice

For more information, visit [Azure OpenAI Service Documentation](https://azure.microsoft.com/en-us/products/ai-services/openai-service/).