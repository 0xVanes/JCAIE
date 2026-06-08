import requests
url = ''
data = {"prompt": "Apa yang dimaksud dengan LLM?"}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code)