from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import os
import cohere
import pytz  # Türkiye saat dilimi için

# Cohere API anahtarını ortam değişkeninden al
cohere_api_key = os.getenv("COHERE_API_KEY", "your-default-key")
co = cohere.Client(cohere_api_key)

app = Flask(__name__)
CORS(app)

# Kullanıcıdan gelen özel komutları kontrol eden fonksiyon
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
        today_eng = datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%A").lower()
        return days.get(today_eng, "Bugünün gününü bilemedim.")
    elif "saat kaç" in voice:
        saat = datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
        return random.choice(["Saat şu an: ", "Hemen bakıyorum: "]) + saat
    else:
        return None

# Cohere üzerinden yapay zeka cevabı alma
def cohere_response(prompt):
    try:
        response = co.chat(
            message=prompt,
            model="command-r-plus",
            temperature=0.7,
            max_tokens=1000
        )
        answer = response.text.strip()
        print("Cohere'den gelen cevap:", answer)
        return answer
    except Exception as e:
        import traceback
        print(">>> Cohere API HATASI <<<")
        print("Hata:", str(e))
        traceback.print_exc()
        return "Şu anda cevap veremiyorum, lütfen sonra tekrar dene."

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
        response = cohere_response(message)
    return jsonify({"reply": response})

# Render uyumlu başlatma
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
