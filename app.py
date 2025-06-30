# app.py (Flask + OpenAI + Sesli Chatbot)
from flask import Flask, render_template, request, jsonify
import openai
from gtts import gTTS
from pydub import AudioSegment 
import os
from datetime import datetime
import random
import webbrowser

# OpenAI API anahtarını buraya koy
openai.api_key = "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"

app = Flask(__name__)

# Ses dosyasını hızlandır (isteğe bağlı)
def speed_swifter(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(
        sound.raw_data,
        overrides={"frame_rate": int(sound.frame_rate * speed)}
    )
    return sound_with_altered_frame_rate

def speeding():
    in_path = 'answer.mp3'
    ex_path = 'audio-4065.mp3'
    sound = AudioSegment.from_file(in_path)
    faster_sound = speed_swifter(sound, 1.1)
    faster_sound.export(ex_path, format="mp3")

def speak(text):
    tts = gTTS(text=text, lang="tr", slow=False)
    file = "answer.mp3"
    tts.save(file)
    speeding()
    os.system("start audio-4065.mp3")  # Windows için
    # Linux/Mac için: os.system("afplay audio-4065.mp3") veya benzeri
    os.remove(file)
    os.remove("audio-4065.mp3")

def openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Türkçe olarak kısa ve anlaşılır cevaplar ver."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        print("OpenAI API Hatası:", e)
        return "Üzgünüm, şu anda cevap veremiyorum."

def check_custom_commands(voice):
    if "merhaba" in voice:
        return "Sana da merhaba genç!"
    elif "selam" in voice:
        return "Sana iki kere selam olsun!"
    elif "teşekkür" in voice:
        return "Rica ederim."
    elif "görüşürüz" in voice:
        return "Görüşmek üzere!"
    elif "bugün günlerden ne" in voice:
        days = {
            "monday": "Pazartesi",
            "tuesday": "Salı",
            "wednesday": "Çarşamba",
            "thursday": "Perşembe",
            "friday": "Cuma",
            "saturday": "Cumartesi",
            "sunday": "Pazar"
        }
        today_eng = datetime.now().strftime("%A").lower()
        return days.get(today_eng, "Bugünün gününü bilemedim.")
    elif "saat kaç" in voice:
        saat = datetime.now().strftime("%H:%M")
        cevaplar = ["Saat şu an: ", "Hemen bakıyorum: "]
        return random.choice(cevaplar) + saat
    elif "google'da ara" in voice:
        return "Bu özellik web tarayıcıda çalışmaz."
    elif "uygulama aç" in voice:
        return "Uygulama açma özelliği bu ortamda devre dışı."
    else:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = check_custom_commands(message)
    if response is None:
        response = openai_response(message)
    speak(response)
    return jsonify({"reply": response})

if __name__ == "__main__:
    app.run(debug=True)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

    
