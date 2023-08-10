import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import pyttsx3
import requests

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 145)
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Di algo...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format='wav')
    except Exception as e:
        print(e)
    return save_path

def recognize_audio(save_path):
    audio_model = whisper.load_model('base')
    transcription = audio_model.transcribe(save_path, language='spanish', fp16=False)   
    return transcription['text']

def get_chat_response(input_text):
    # URL de la API de ChatGPT
    api_url = 'https://api.openai.com/v1/chat/completions'

    # Token de autenticación de la API
    api_key = 'key'

    # Cabeceras de la solicitud HTTP
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Datos de la solicitud HTTP
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'Eres un asistente de voz.'},
                     {'role': 'user', 'content': input_text}]
    }

    # Realizar la solicitud HTTP POST a la API
    response = requests.post(api_url, headers=headers, json=data)

    # Obtener la respuesta de la API
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Error al acceder a la API de ChatGPT'

def main():
    response = recognize_audio(listen())
    #talk(response)
    print(response)
    
    # Consulta a la API
    pregunta = response
    respuesta = get_chat_response(pregunta)
    print(respuesta)
    talk(respuesta)
    

if __name__ == '__main__':
    main()

