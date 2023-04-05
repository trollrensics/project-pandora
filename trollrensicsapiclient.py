import os
import requests

def retrieve_tiktok_video_data(tt_url):
    headers = {
        'Authorization': f'Bearer {os.environ["TROLLRENSICS_API_KEY"]}',
    }
    endpoint = f"https://api.trollrensics.com/api/v2/retrievemedia/"
    payload = {
        'platform': 'tiktok',
        'tt_url': tt_url,
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Error: Unable to fetch data from {endpoint}. Status code: {response.status_code}")
        return None

