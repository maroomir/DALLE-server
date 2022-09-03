import base64
from io import BytesIO

import requests
from PIL import Image
import matplotlib.pyplot
import numpy

import metaartserver


def decode_image(data: dict):
    res = []
    for i, img_encode in enumerate(data):
        print(f'=> Receive({i}) : {img_encode}')
        res.append(Image.open(BytesIO(base64.b64decode(img_encode))))
    return res


def show_image(imgs: list, width=10, height=50):
    imgs = numpy.concatenate(imgs, axis=1)
    matplotlib.pyplot.figure(figsize=(width, height))
    matplotlib.pyplot.imshow(imgs)


def run_dalle(num_images: int, text: str):
    input_ = {'num_images': num_images,
              'text': text}
    res = requests.post(server + '/dalle', json=input_)
    if 200 <= res.status_code < 300:
        imgs = decode_image(res.json())
        show_image(imgs)


if __name__ == "__main__":
    server = f'http://{metaartserver.TEST_INTERNAL_SERVER}:{metaartserver.TEST_INTERNAL_PORT}'
    res = requests.get(server + '/health')
    print(res.content)
    run_dalle(num_images=5, text='smiling woman')
