import requests
from docx import Document
from pathlib import Path

# Eleven Labs API Configuration
API_KEY = "sk_7647aed4f8d3e678d461472ecbfb5daaf261d0f5f10d1c9a"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Replace this with your actual voice ID
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

# File and voice configuration
DOCX_FILE_NAME = "Cooking_Script_2024-12-30.docx"
OUTPUT_FILE_NAME = "output_voice.mp3"
CHUNK_SIZE = 1024 * 1024  # 1 MB

# Function to read the text from a DOCX file
def read_docx(file_name):
    try:
        document = Document(file_name)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None

# Function to send text to Eleven Labs API and generate audio
def text_to_voice(text):
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # Specify the model
        "voice_settings": {
            "stability": 0.75,  # Optional: Adjust voice stability
            "similarity_boost": 0.75  # Optional: Adjust voice similarity
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, stream=True)
        response.raise_for_status()

        # Write the audio content in chunks to the output file
        with open(OUTPUT_FILE_NAME, "wb") as audio_file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    audio_file.write(chunk)

        print(f"Voice file saved as '{OUTPUT_FILE_NAME}'")
    except requests.exceptions.RequestException as e:
        print(f"Error generating voice: {e}")

# Main function to execute the script
def main():
    # Check if the DOCX file exists
    file_path = Path(DOCX_FILE_NAME)
    if not file_path.exists():
        print(f"File not found: {DOCX_FILE_NAME}")
        return

    # Read the text from the DOCX file
    text = read_docx(DOCX_FILE_NAME)
    if not text:
        print("No text found in the DOCX file or failed to read the file.")
        return

    # Convert the text to audio
    text_to_voice(text)

# Entry point of the script
if __name__ == "__main__":
    main()
