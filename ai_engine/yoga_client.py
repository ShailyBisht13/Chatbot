# yoga_client.py — FINAL, STRICT VERSION (NO FAKE RESPONSES)

import requests


def detect_yoga(image_path):
    try:
        with open(image_path, "rb") as img:
            response = requests.post(
                "http://127.0.0.1:5005/predict",
                files={"image": img},
                timeout=5
            )

        # 🔥 RETURN EXACT SERVER RESPONSE ONLY
        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "pose": "Yoga service offline",
            "feedback": [
                "✘ Yoga AI service is not running.",
                "✔ Please start yoga_server.py and try again."
            ]
        }

    except Exception as e:
        return {
            "pose": "Yoga error",
            "feedback": [str(e)]
        }
