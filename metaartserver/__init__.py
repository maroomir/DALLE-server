import os.path
import time
from queue import Queue, Empty
from threading import Thread

from flask import Flask, jsonify, request

from metaartserver.dalle import generate

REQUEST_BATCH_SIZE = 4
PROCESS_IMAGE_CNT = 10
CHECK_INTERVAL = 0.1

REQUEST_ERR_REQUESTS_OVER = {'Error': 'Too Many Requests. Please try again layer'}
REQUEST_ERR_IMAGES_OVER = {'Error': f'Too Many Images requested. Request no more than {PROCESS_IMAGE_CNT}'}
REQUEST_ERR_INVALID = {'Error': 'Invalid Request'}
REQUEST_ERR_GENERATE = {'Error': 'Image Generate Error'}

TEST_INTERNAL_SERVER = '127.0.0.1'
TEST_INTERNAL_PORT = '5000'


def dalle_requests_handle(queue, model_path):
    while True:
        batch = []
        while not (len(batch) >= REQUEST_BATCH_SIZE):
            try:
                batch.append(queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue
            for req in batch:
                try:
                    text, num_images = req['input'][0], req['input'][1]
                    req['output'] = generate(text, num_images, model_path=model_path)
                except:
                    req['output'] = jsonify(REQUEST_ERR_GENERATE), 500


def create_app(dalle_path: str):
    app = Flask(__name__)
    queue = Queue()
    if not os.path.exists(dalle_path):
        raise ReferenceError(f"DALL-E Model ({dalle_path}) is not exists")
    dalle_worker = Thread(target=dalle_requests_handle, args=(queue, dalle_path))
    dalle_worker.start()

    @app.route('/dalle', methods=['POST'])
    def generate_dalle():
        if queue.qsize() > REQUEST_BATCH_SIZE:
            return jsonify(REQUEST_ERR_REQUESTS_OVER), 429
        try:
            inputs = []
            json_data = request.get_json()
            text, num_images = json_data['text'], json_data['num_images']
            if num_images > 10:
                return jsonify(REQUEST_ERR_IMAGES_OVER), 500
            inputs.append(text)
            inputs.append(num_images)
        except Exception:
            return jsonify(REQUEST_ERR_INVALID), 500

        req = {'input': inputs}
        queue.put(req)
        while 'output' not in req:
            time.sleep(CHECK_INTERVAL)
        return jsonify(req['output'])

    @app.route('/health', methods=['GET'])
    def check_health():
        return "Health", 200

    return app
