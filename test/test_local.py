import os
import argparse
import json
import requests
import numpy as np
from imageio import imwrite

parser = argparse.ArgumentParser(description='Please provide a path to a jpg file.')
parser.add_argument('ImgPath',
   metavar='path',
   type=str,
   help='the path to the jpg image')

args = parser.parse_args()
img_path = args.ImgPath

payload = ''
with open(img_path, 'rb') as f:
    payload = f.read()
    payload = bytearray(payload)
    
URL = 'http://127.0.0.1:8080/invocations'

headers = {'Content-type': 'application/x-image'}
resp = requests.post(URL, data=payload, headers=headers)


data = json.loads(resp.content)
cropped_img = np.array(data['img_lp'])
cropped_img = cropped_img[0]
coords = np.array(data['coords_lp'])

print(cropped_img.shape)

imwrite('inference.jpg', cropped_img)