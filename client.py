import requests
import os
import mimetypes


BASE_URL = "http://127.0.0.1:8000"


def basic_request(image_path: str):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            mime_type, _ = mimetypes.guess_type(image_path)
            files = {"file": (os.path.basename(image_path), image_file, mime_type)}

            response = requests.post(f"{BASE_URL}/upload/", files=files)

        if response.status_code == 201:          
            list_response = requests.get(f"{BASE_URL}/images/")
            if list_response.status_code == 200:
                
                image_id = response.json()["id"]
                get_response = requests.get(f"{BASE_URL}/images/{image_id}")
                if get_response.status_code == 200:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
