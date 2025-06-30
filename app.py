# app.py (Render uyumlu, ses çalma olmadan, CORS dahil)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from datetime import datetime
import random
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Render'da gizli key kullan

app = Flask(__name__)
CORS(app)

# Mesajlara özel komutlar

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
        return random.choice(["Saat şu an: ", "Hemen bakıyorum: "]) + saat
    else:
        return None

# OpenAI'dan cevap alma fonksiyonu

def openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # veya "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Türkçe olarak kısa ve anlaşılır cevaplar ver."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("API hatası:", e)
        return "Üzgünüm, şu anda cevap veremiyorum."

# Anasayfa
@app.route("/")
def index():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = check_custom_commands(message)
    if response is None:
        response = openai_response(message)
    print("Cevap:", response)  # DEBUG
    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
