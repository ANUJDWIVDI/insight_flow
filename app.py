from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

# Simulated user credentials for demonstration purposes sa
VALID_USERNAME = '123'
VALID_PASSWORD = '123'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    r = sr.Recognizer()

    try:
        # Assuming you have an audio file uploaded through a form
        uploaded_file = request.files['audio_file']

        # Check if the file exists and is not empty
        if not uploaded_file or uploaded_file.filename == '':
            return render_template('result.html', text="No file uploaded")

        # Convert the audio file to PCM WAV format
        converted_audio = convert_to_pcm_wav(uploaded_file)

        with sr.AudioFile(converted_audio) as source:
            audio_text = r.listen(source)

        # Check the duration of the audio file
        audio_duration = source.DURATION

        # Check if the audio file is too short
        if audio_duration < 1.0:
            return render_template('result.html', text="Audio file is too short")

        text = r.recognize_google(audio_text)
        return render_template('result.html', text=text)

    except sr.UnknownValueError:
        return render_template('result.html', text="Could not understand audio")

    except sr.RequestError as e:
        return render_template('result.html', text=f"Error connecting to Google API: {e}")

    except Exception as e:
        return render_template('result.html', text=f"Error processing audio: {e}")

def convert_to_pcm_wav(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file, format=uploaded_file.filename.split('.')[-1])
    converted_audio = audio.export("converted_audio.wav", format="wav")
    return "converted_audio.wav"

if __name__ == '__main__':
    app.run(debug=True)
