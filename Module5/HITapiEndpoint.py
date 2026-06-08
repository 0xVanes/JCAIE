import requests

# Masukin url webhooknya disini
url = 'https://n8n-student.purwadhika.com/webhook/trying1'

data = {"age": "12"}
# post = post webhook di n8n (sesuaiin)
respond = requests.post(url, data=data)
print(respond.status_code)
# 100 = informasional (continue, processing, switching protocols)
# 200 = success code complete guide (ok, created, accepted)
# 300 = redirect codes and their uses
# 400 = Client Error (Devs yg salah)
# 500 = Disconnected atau salah waktu lg connect (server error)
if respond.status_code == 200:
    result = respond.json()
    print(result)
else:
    print(respond.status_code)
    print('Gagal mengambil data')