import requests
from config import API_KEY, PROJECT


def identify_plant(image_path):

    url = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

    files = {
        "images": open(image_path, "rb")
    }

    data = {
    "organs": ["auto"]
       }

    response = requests.post(url, files=files, data=data)

    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()