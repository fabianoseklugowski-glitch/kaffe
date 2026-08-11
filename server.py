from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="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")

URL_FIRMY = "https://fabianoseklugowski-glitch.github.io/kaffe/indexkaffe.html"
print(f"Pobieram wiedzę ze strony: {URL_FIRMY}...")

try:
    res = requests.get(URL_FIRMY, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    baza_wiedzy = soup.get_text(separator="\n", strip=True)
    print("Baza wiedzy załadowana pomyślnie!")
except Exception as e:
    baza_wiedzy = "Brak danych."

messages = [
    {"role": "system", "content": f"Jesteś miłym asystentem na stronie kawiarni. Oto informacje ze strony:\n\n{baza_wiedzy}"}
]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"reply": "Brak wiadomości"})
        
    messages.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    bot_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_reply})
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(port=5000, debug=True)