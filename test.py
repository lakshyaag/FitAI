import requests
from main import Request

answers = """{"answer": {
  "1": "18-24",
  "2": "Male",
  "3": 180,
  "4": 79,
  "5": "Beginner",
  "6": "No",
  "7": "4 days",
  "8": "Gain muscle",
  "9": "Gym",
  "10": "Arms",
  "11": "Full-body workouts",
  "12": "Bodyweight exercises",
  "13": "No",
  "14": "",
  "15": "Less than 30 minutes",
  "16": [
    "Dumbbells",
    "Barbells"
  ],
  "17": "",
  "18": "3 months"
}}"""

query = "Give me a list of 50 random colors"
url = "http://localhost:5000/generate"

with requests.post(
    url, data=answers, headers={"Content-Type": "application/json"}, stream=True
) as r:
    for chunk in r.iter_lines():  # or, for line in r.iter_lines():
        print(chunk.decode("utf-8"))
