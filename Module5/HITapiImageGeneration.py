import base64
from IPython.display import Image, display
import requests

url = ''
prompt_text = 'Buatkan gambar astronot di Mars'
prompt_enhancement = True

payload = { "prompt_text": prompt_text,
           "prompt_enhancement": prompt_enhancement}

response = requests.post(url, json=payload)
data_response = response.json()
image_base64 = data_response['data']
display(Image(data=base64.b64decode(image_base64)))