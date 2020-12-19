import argparse
import os
import boto3
import json
import numpy as np
from imageio import imwrite

endpoint_name = os.environ['SM_ENDPOINT_NAME']

parser = argparse.ArgumentParser(description='Please provide a path to a jpg file.')
parser.add_argument('img_path', metavar='path', type=str, help='the path to the jpg image')
parser.add_argument('-o', '--output', metavar='output', type=str, default='inference.jpg', help='the output path of the jpg image')

args = parser.parse_args()
img_path = args.img_path
output_path = args.output

payload = ''
with open(img_path, 'rb') as f:
    payload = f.read()
    payload = bytearray(payload)
    
print('Calling SageMaker Endpoint...')
sm = boto3.client('sagemaker-runtime')
resp = sm.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/x-image',
    Body=payload
)

# Read response bytestream body
resp_body = resp['Body'].read()

# Extract json
data = json.loads(resp_body)
cropped_img = np.array(data['img_lp'])
cropped_img = cropped_img[0]
coords = np.array(data['coords_lp'])

# Write image
print('Writing respone image to ' + output_path)
imwrite(output_path, cropped_img)