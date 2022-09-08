import os.path

from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok

from metaartserver.dalle import generate
from metaartserver.data import getter

REQUEST_BATCH_SIZE = 4
PROCESS_IMAGE_CNT = 10
CHECK_INTERVAL = 0.1

REQUEST_ERR_IMAGES_OVER = {'Error': f'Too Many Images requested. Request no more than {PROCESS_IMAGE_CNT}'}
REQUEST_ERR_INVALID = {'Error': 'Invalid Request'}
REQUEST_ERR_GENERATE = {'Error': 'Image Generate Error'}
REQUEST_ERR_GET = {'Error': 'Get Images Error'}

TEST_INTERNAL_SERVER = '127.0.0.1'
TEST_INTERNAL_PORT = '5000'

DEFAULT_IMAGE_SIZE = (256, 256)

IMG_FORMAT = ['.jpg', '.bmp', '.png']


def create_app(dalle_path: str, data_path: str):
    app = Flask(__name__)
    # run_with_ngrok(app)
    if not os.path.exists(dalle_path):
        raise ReferenceError(f"DALL-E Model ({dalle_path}) is not exists")
    if not os.path.exists(data_path):
        raise ReferenceError(f"Data Folder ({data_path}) is not exists")

    @app.route('/dalle', methods=['POST'])
    def generate_dalle():
        try:
            json_data = request.get_json()
            text, num_images = json_data['text'], json_data['num_images']
            if num_images > 10:
                return jsonify(REQUEST_ERR_IMAGES_OVER), 500
            res = dalle.generate(text, num_images, model_path=dalle_path)
            if not isinstance(res, list):
                return jsonify(REQUEST_ERR_GENERATE), 500
            else:
                return jsonify(res), 200
        except:
            return jsonify(REQUEST_ERR_INVALID), 500

    @app.route('/health', methods=['GET'])
    def check_health():
        return "OK", 200

    @app.route('/images/<count>', methods=['GET'])
    def get_images(count):
        try:
            res = getter(int(count), img_path=data_path, trace=True)
            if not isinstance(res, list):
                return jsonify(REQUEST_ERR_GET), 500
            else:
                return jsonify(res), 200
        except:
            return jsonify(REQUEST_ERR_INVALID), 500

    return app
