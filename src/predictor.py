import os
import json
import flask
from keras.models import model_from_json
import logging
import cv2
import numpy as np
import utils

MODEL_PATH = '/opt/ml/'
TMP_MODEL_PATH = '/tmp/ml/model'
DATA_PATH = '/tmp/data'
MODEL_FILENAME = 'model.json' 
WEIGHTS_FILENAME = 'weights.h5'

IMG_FOR_INFERENCE = os.path.join(DATA_PATH, 'image_for_inference.jpg')

# in this tmp folder, image for inference will be saved
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH, mode=0o755,exist_ok=True)
    
def write_test_image(stream):
    with open(IMG_FOR_INFERENCE, "bw") as f:
        chunk_size = 4096
        while True:
            chunk = stream.read(chunk_size)
            if len(chunk) == 0:
                return
            f.write(chunk)

class ClassificationService(object):
    def __init__(self, path):
        self.model = None
        try:
            modeljson_path = os.path.join(path, MODEL_FILENAME)
            weightsjson_path = os.path.join(path, WEIGHTS_FILENAME)
            print('ModelPath=' + modeljson_path)
    
            with open(modeljson_path, 'r') as json_file:
              model_json = json_file.read()
            self.model = model_from_json(model_json, custom_objects={})
            self.model.load_weights(weightsjson_path)
            print('Loaded model sucessfully!')
        except Exception as e:
            print(e)
            raise Exception('Reading model failed.')
    
    def get_model(self):
        return self.model
    
    def predict(self, img):
        img = self._preprocess(img)
        return self.model.predict(img)
        
    def _preprocess(self, img):
        max_dim = 608
        min_dim_img = min(img.shape[:2])
        factor = float(max_dim) / min_dim_img
        w, h = (np.array(img.shape[1::-1], dtype=float) * factor).astype(int).tolist()
        img_resized = cv2.resize(img, (w, h))
        img_cpy = img_resized.copy()
        img_cpy = img_cpy.reshape((1, img_cpy.shape[0], img_cpy.shape[1], img_cpy.shape[2]))
        return img_cpy
        
    def predict_and_reconstruct(self, img):
        """Process according to Github repo"""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255
        
        max_dim = 608
        min_dim_img = min(img.shape[:2])
        factor = float(max_dim) / min_dim_img
        w, h = (np.array(img.shape[1::-1], dtype=float) * factor).astype(int).tolist()
        img_resized = cv2.resize(img, (w, h))
        img_cpy = img_resized.copy()
        img_cpy = img_cpy.reshape((1, img_cpy.shape[0], img_cpy.shape[1], img_cpy.shape[2]))
        Y = self.model.predict(img_cpy)
        Y = np.squeeze(Y)
        L, TLp, lp_type, Cor = utils.reconstruct(img, img_resized, Y, 0.5)
        return L, TLp, lp_type, Cor

#Define the path
model_path = os.path.join(MODEL_PATH, 'model')
print("Model Path Base: " + str(model_path))

# Load the model components
clf = ClassificationService(model_path)

# The flask app for serving predictions
app = flask.Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        #regressor
        status = 200
        logging.info("Status : 200")
    except:
        status = 400
    return flask.Response(response= json.dumps(' '), status=status, mimetype='application/json' )

@app.route('/invocations', methods=['POST'])
def transformation():
    
    write_test_image(flask.request.stream)
    img = cv2.imread(IMG_FOR_INFERENCE)
    L, TLp, lp_type, coors = clf.predict_and_reconstruct(img)

    # Transform predictions to JSON
    result = {
        'img_lp': (np.array(TLp)).tolist(),
        'coords_lp': (np.array(coors)).tolist()
        }

    resultjson = json.dumps(result)
    return flask.Response(response=resultjson, status=200, mimetype='application/json')