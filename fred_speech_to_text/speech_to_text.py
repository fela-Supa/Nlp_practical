"""
=================================================================================================
Python script to demonstrate Speech-to-Text using the SpeechRecognition package
=================================================================================================
This program demonstrates Speech-to-Text using the SpeechRecognition package

Flow:
    1. Read in an audio file (.wav)
    2. Process the audio in a Python program
    3. Speech-to-Text Engine transcribes the audio to text
    4. Output a text file (travel_transcript.txt) and print the transcript on screen

Input / Output file locations:
    - input: files/travel_output.wav
    - output: files/travel_transcript.txt

Requirements:
    !pip install SpeechRecognition
"""

# -----------------------------------------------------------------------------------------------
# 0. Import required modules
# -----------------------------------------------------------------------------------------------
import logging #(optional to show what is happening at what time)
import sys

from pathlib import Path

import warnings

import speech_recognition as sr

# Suppress warnings for cleaner output demo
warnings.filterwarnings("ignore")

# -------------------------------------------
# 1. Optional Logging Configuration
# -------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
)

logger = logging.getLogger(__name__)

# -------------------------------------------
# 2. Constants
# -------------------------------------------
AUDIO_FILE: Path = Path("../files/travel_output.wav")
OUTPUT_FILE: Path = Path("../files/transcribed_speech.txt")

LANGUAGE = "en-US"

# -------------------------------------------
# 3. Functions
# -------------------------------------------
def load_audio(file_path: Path) -> sr.AudioFile:

    logger.info(f"Loading audio from {file_path}...")

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found at {file_path} "
            f"\nPlease ensure that 'travel_output.wav' exists in the folders project structure."
        )

    logger.info(f"Successfully located audio file at {file_path}.")
    return sr.AudioFile(str(file_path))

def initialise_recogniser() -> sr.Recognizer:

    logger.info(f"Initialising STT recogniser...")

    try:
        recognizer = sr.Recognizer()
    except Exception as ex:
        raise RuntimeError(
            f"Failed to initialise STT recogniser."
            f"\nPlease ensure that 'SpeechRecognition' is installed in your system: pip install SpeechRecognition"
        ) from ex

    logger.info(f"Recogniser ready | Language: {LANGUAGE}")
    return recognizer


def transcribe_audio(recogniser: sr.Recognizer, audio_source: sr.AudioFile, language: str) -> str:

    logger.info(f"Transcribing audio...")

    # Reading the entire file into an Audiodata object
    with audio_source as source:
        audio_data = recogniser.record(source)

    try:
        text: str = recogniser.recognize_google(audio_data, language=language)
    except sr.UnknownValueError as ex:
        raise ValueError(
            f"Speech recognision could not understand the audio."
            f"\nPlease check that the .wav file contains clear speech."
        )from ex
    except sr.RequestError as ex:
        raise ConnectionError(
            f"Could not request results from the Google Web Speech API: {ex}"
            f"\n Please check your internet connection and try again."
        ) from ex

    logger.info(f"Transcribing complete.")
    return text

def save_transcript(text: str, output_path: Path) -> None:

    logger.info(f"Saving transcript to {output_path}...")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(text, encoding="utf-8")

    if not output_path.exists():
        raise IOError(
            f"Transcription file was not created at: '{output_path}'"
            f"\nPlease ensure that Python has permissions to write to the 'files' folder."
        )
    logger.info(f"Successfully saved transcript to {output_path}.")


# -------------------------------------------
# 4. Main Execution Function
# -------------------------------------------
def main() -> None:
    print()
    print("-" * 50)
    print(" SPEECH TO TEXT DEMONSTRATION")
    print("-" * 50)
    print()

    # -------------------------------------------
    # I. Load Audio File
    # -------------------------------------------
    print("Loading audio...")
    try:
        audio_source = load_audio(AUDIO_FILE)
    except FileNotFoundError as ex:

        logger.error(f"COuld not load audio: {ex}")
        sys.exit(1)

    # -------------------------------------------
    # II. Initialise the recogniser
    # -------------------------------------------
    try:
        recogniser: sr.Recognizer = initialise_recogniser()
    except RuntimeError as ex:
        logger.error(f"Failed to initialise recogniser: {ex}")
        sys.exit(1)

    # -------------------------------------------
    # III. Load Audio File
    # -------------------------------------------
    print("Transcribing speech to text...\n")
    try:
        transcript = transcribe_audio(recogniser, audio_source, LANGUAGE)
    except (ValueError, ConnectionError) as ex:
        logger.error(f"Cold not transcribe audio: {ex}")
        sys.exit(1)

    # -------------------------------------------
    # IV. Display th transcript on screen
    # -------------------------------------------
    print()
    print("-" * 50)
    print("     TRANSCRIPT     ")
    print("-" * 50)
    print(transcript)
    print("-" * 50)
    print()

    # -------------------------------------------
    # V. Save the transcript to a .txt file
    # -------------------------------------------
    try:
        save_transcript(transcript, OUTPUT_FILE)
    except IOError as ex:

        logger.error(f"Could not save transcript file: {ex}")
        sys.exit(1)

    print(f"Transcript saved to {OUTPUT_FILE}\n")
    print("\nEND OF DEMONSTRATION\n")


# -----------------------------------------------------
# 5. Run the script by invoking it's main() function
# -----------------------------------------------------
if __name__ == "__main__":
    main()