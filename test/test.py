import os
import json
import requests

payload = ''
with open('img.jpg', 'rb') as f:
    payload = f.read()
    payload = bytearray(payload)
    
URL = 'http://127.0.0.1:8080/invocations'

headers = {'Content-type': 'application/x-image'}
resp = requests.post(URL, data=payload, headers=headers)

print(resp.content)