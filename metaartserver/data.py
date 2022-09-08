import base64

import os
import random
from io import BytesIO

from tqdm import tqdm
from PIL import Image
import metaartserver


def getter(count: int, img_path='', trace=False):
    try:
        inputs = []
        for root, _, files in os.walk(img_path):
            inputs += [os.path.join(root, f) for f in files \
                       if os.path.splitext(f)[-1] in metaartserver.IMG_FORMAT]
        if count > len(inputs):
            count = len(inputs)
        outputs = random.sample(inputs, count)
        print(f'Sampling the {count} images')
        response = []
        iters = enumerate(outputs) if trace else tqdm(enumerate(outputs), desc='wrapping images')
        for i, im_path in iters:
            img = Image.open(im_path)
            img = img.resize(size=metaartserver.DEFAULT_IMAGE_SIZE)
            img = img.convert(mode='RGB')
            if trace:
                print(f'path{i} = {im_path}')
            # encode the image to the string for the request
            buffered = BytesIO()
            img.save(buffered, format='JPEG')
            img_encode = base64.b64encode(buffered.getvalue()).decode('utf-8')
            response.append(img_encode)
        if trace:
            for i, img_encode in enumerate(response):
                print(f'send({i}) => {img_encode}')
        return response
    except Exception as ex:
        print('Error occur in get images!\n', ex)
        raise ChildProcessError(ex)
