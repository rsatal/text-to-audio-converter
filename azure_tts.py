import os
import openai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def text_to_speech(text, output_file="output.wav", 
                   api_key=None, endpoint=None, 
                   api_version="2025-01-01-preview",
                   model_name="tts-1",
                   voice_name="alloy",
                   speech_rate=1.0):
    """
    Convert text to speech using Azure OpenAI TTS.
    
    Args:
        text (str): The text to convert to speech
        output_file (str): Path to the output audio file
        api_key (str): Azure OpenAI API key
        endpoint (str): Azure OpenAI endpoint URL
        api_version (str): API version to use
        model_name (str): Name of the deployed model in Azure OpenAI
        voice_name (str): Name of the voice to use
        speech_rate (float): Speed of speech (1.0 is normal, >1.0 is faster, <1.0 is slower)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Use environment variables if not explicitly provided
    api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = api_version or os.environ.get("API_VERSION", "2025-01-01-preview")
    model_name = model_name or os.environ.get("AZURE_OPENAI_TTS_DEPLOYMENT", "gpt-4o-mini-tts")
    
    if not api_key or not endpoint:
        print("Error: Azure OpenAI API key and endpoint are required.")
        print("Either pass them as parameters or set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables.")
        return False
    
    # Configure OpenAI client with Azure settings
    client = openai.AzureOpenAI(
        api_key=api_key,  
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    print(f"Converting text to speech... Output file: {output_file}")
    print(f"Using model: {model_name}, voice: {voice_name}, speed: {speech_rate}x")
    
    try:
        # Create speech using the deployed model with speed parameter
        audio_response = client.audio.speech.create(
            model=model_name,
            voice=voice_name,
            input=text,
            speed=speech_rate
        )
        
        # Save the audio to a file
        audio_response.stream_to_file(output_file)
        
        print(f"Speech synthesized successfully. Audio saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error in speech synthesis: {str(e)}")
        return False

def read_text_from_file(file_path):
    """
    Read text content from a file
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        str: Text content from the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert text to speech using Azure OpenAI.")
    parser.add_argument("text", nargs="?", help="The text to convert to speech or file path when using --from-file")
    parser.add_argument("output_file", nargs="?", default="output.wav", help="Output audio file path")
    parser.add_argument("--voice", "-v", default="alloy", help="Voice name (alloy, echo, fable, onyx, nova, shimmer)")
    parser.add_argument("--speed", "-s", type=float, default=1.0, help="Speech rate (1.0 is normal, 1.2 is 20%% faster)")
    parser.add_argument("--model", "-m", default="gpt-4o-mini-tts", help="Model name for TTS")
    parser.add_argument("--from-file", "-f", action="store_true", help="Read text from the specified file")
    
    if len(sys.argv) > 1:
        args = parser.parse_args()
        
        if args.text:
            # Get the text content - either direct or from a file
            if args.from_file:
                content = read_text_from_file(args.text)
                if content is None:
                    sys.exit(1)
            else:
                content = args.text
                
            text_to_speech(content, args.output_file, 
                         voice_name=args.voice, 
                         speech_rate=args.speed,
                         model_name=args.model)
        else:
            parser.print_help()
    else:
        print("Usage examples:")
        print("  1. Direct text: python azure_tts.py \"Text to convert\" output.wav")
        print("  2. From file: python azure_tts.py input.txt output.wav --from-file")