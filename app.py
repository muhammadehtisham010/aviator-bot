from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_latest_crash_values():
    url = "https://b9.game"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    crash_elements = soup.find_all("li", class_="av2-c-past-result-list__tile clickable")
    crash_values = []

    for el in crash_elements[:10]:  # Get last 10 values
        text = el.get_text(strip=True).replace("x", "")
        try:
            crash_values.append(float(text))
        except:
            continue
    return crash_values

def predict_next(crash_list):
    if len(crash_list) < 2:
        return "Not enough data"

    last = crash_list[0]
    prev = crash_list[1]

    if last < 2 and prev < 2:
        return "Safe Bet Likely"
    elif last > 10:
        return "Crash Likely"
    else:
        return "Neutral Round"

@app.route("/predict", methods=["GET"])
def predict():
    values = get_latest_crash_values()
    prediction = predict_next(values)
    return jsonify({
        "last_crashes": values,
        "prediction": prediction
    })

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
