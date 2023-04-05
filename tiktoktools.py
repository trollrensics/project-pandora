import requests
import os

def get_final_url(url):
    response = requests.get(url, allow_redirects=True)
    final_url = response.url
    return final_url

def get_and_save_page(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)