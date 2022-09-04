import os.path
import time

from flask import Flask, jsonify, request

from metaartserver.dalle import generate

REQUEST_BATCH_SIZE = 4
PROCESS_IMAGE_CNT = 10
CHECK_INTERVAL = 0.1

REQUEST_ERR_IMAGES_OVER = {'Error': f'Too Many Images requested. Request no more than {PROCESS_IMAGE_CNT}'}
REQUEST_ERR_INVALID = {'Error': 'Invalid Request'}
REQUEST_ERR_GENERATE = {'Error': 'Image Generate Error'}

TEST_INTERNAL_SERVER = '127.0.0.1'
TEST_INTERNAL_PORT = '5000'


def create_app(dalle_path: str):
    app = Flask(__name__)
    if not os.path.exists(dalle_path):
        raise ReferenceError(f"DALL-E Model ({dalle_path}) is not exists")

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
                return res
        except:
            return jsonify(REQUEST_ERR_INVALID), 500

    @app.route('/health', methods=['GET'])
    def check_health():
        return "Health", 200

    return app
