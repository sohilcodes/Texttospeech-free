from flask import Flask, request, render_template, send_file
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    languages = {
        "hi": "Hindi",
        "en": "English",
        "en-in": "Hinglish"
    }
    return render_template("index.html", languages=languages)

@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    lang = request.form.get("language")
    
    if not text or not lang:
        return "Text and language are required.", 400

    file_name = f"/tmp/{uuid.uuid4()}.mp3"
    
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(file_name)
    except Exception as e:
        return f"Error generating audio: {e}", 500

    return send_file(file_name, as_attachment=True, download_name="speech.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
