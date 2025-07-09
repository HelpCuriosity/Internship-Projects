import speech_recognition as sr
import os
from datetime import datetime

def transcribe_from_microphone(lang='en-IN', speak_time=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"\nSpeak now... You have {speak_time} seconds to speak.")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=speak_time)
            print('Recognizing...')
            text = recognizer.recognize_google(audio, language=lang)
            print("\nTranscribed Text: ", text)
            save_transcription(text)
        except sr.WaitTimeoutError:
            print("You took too long to start speaking.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from the API.")

def transcribe_from_file(file_path, lang='en-IN'):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language=lang)
            print("\nTranscribed Text: ", text)
            save_transcription(text)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print("Error in processing the file: ", e)

def save_transcription(text):
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'transcripts/transcription_{timestamp}.txt'

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'\nTranscription saved to {file_name}')

def main():
    print("\n=== Speech-to-Text Transcription Tool ===")
    print("Options:")
    print("1. Transcribe from Microphone")
    print("2. Transcribe from Audio File")

    choice = input("Enter your choice (1 or 2): ")

    lang = input("\nEnter the language code (default 'en-IN'): ") or 'en-IN'

    if choice == '1':
        try:
            speak_time = int(input("Enter the time limit for speaking (in seconds): "))
        except ValueError:
            print("Invalid input. Using default 5 seconds.")
            speak_time = 5
        transcribe_from_microphone(lang, speak_time)
    elif choice == '2':
        file_path = input("Enter the path to the audio file: ")
        transcribe_from_file(file_path, lang)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
