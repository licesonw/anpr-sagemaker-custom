import os
import json
import requests
import numpy as np
from imageio import imwrite

IMAGE = 'germany_car_plate.jpg'
payload = ''

with open(IMAGE, 'rb') as f:
    payload = f.read()
    payload = bytearray(payload)
    
URL = 'http://127.0.0.1:8080/invocations'

headers = {'Content-type': 'application/x-image'}
resp = requests.post(URL, data=payload, headers=headers)


#print(resp.content)
data = json.loads(resp.content)
cropped_img = np.array(data['TLp'])
cropped_img = cropped_img[0]
coords = np.array(data['coors'])

print(cropped_img.shape)

imwrite('inference.jpg', cropped_img)