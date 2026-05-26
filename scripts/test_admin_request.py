import requests

r = requests.get('http://127.0.0.1:8000/admin/')
print('STATUS', r.status_code)
print(r.text[:4000])
