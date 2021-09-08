import requests
import datetime as dt
import os

NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_API = "https://api.sheety.co/cfa2b9b0fbafe2e581aff5ed1630dd82/myWorkouts/workouts"
NUTRITIONIX_API_KEY = os.getenv("NT_API_KEY")
AUTH_TOKEN_SHEETS = os.getenv("AUTH_TOKEN")
APP_ID = os.getenv("TOKEN")

# nutritionix header
headers = {
    "x-app-id": APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "x-remote-user-id": "0",
}
# nutrionix json params
parameters = {
    "query": input("What workout did you do today?: "),
    "gender": "female",
    "weight_kg": 52,
    "height_cm": 159,
    "age": 20,
}
# Bearer Token Authentication
bearer_auth_header = {
    "Authorization": f"Bearer {AUTH_TOKEN_SHEETS}"
}

nutrionix_response = requests.post(NUTRITIONIX_ENDPOINT, json=parameters, headers=headers)
exercise_data = nutrionix_response.json()["exercises"]
print(exercise_data)

for exercise in exercise_data:
    today = dt.datetime.now()
    sheety_parameters = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%I:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheety_response = requests.post(SHEETY_API, json=sheety_parameters, headers=bearer_auth_header)
    print(sheety_response.text)