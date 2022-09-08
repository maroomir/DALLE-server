import base64

import torch
import numpy

from dalle_pytorch.tokenizer import tokenizer
from dalle_pytorch import DALLE, VQGanVAE
from einops import repeat
from tqdm import tqdm
from PIL import Image
from io import BytesIO


def load_model(path: str, device: str):
    model_data = torch.load(path, map_location=device)
    # clean-up the VAE model for using VQGan at this model
    dalle_params, _, weights = model_data.pop('hparams'), model_data.pop('vae_params'), model_data.pop('weights')
    dalle_params.pop('vae', None)
    # load the VAE
    vae = VQGanVAE(None, None)
    # load the DALLE
    model = DALLE(vae=vae, **dalle_params).cuda()
    model.load_state_dict(weights)
    return model


def generate(text,
             num_images,
             model_path: str,
             batch_size=4,
             thresh=0.9,
             trace=False):
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    try:
        # load the DALLE model
        dalle = load_model(model_path, device=device)
        # tokenize the input texts
        text_token = tokenizer.tokenize([text], dalle.text_seq_len).to(device)
        text_token = repeat(text_token, '() n -> b n', b=num_images)
        response, outputs = [], []
        for x in tqdm(text_token.split(batch_size), desc=f'generating images for - {text_token}'):
            # generate the image with input tokens
            y = dalle.generate_images(x, filter_thres=thresh)
            outputs.append(y)
        outputs = torch.cat(outputs)
        for i, y in tqdm(enumerate(outputs), desc='saving images'):
            # convert the output to the image with 8bit scales
            y = numpy.moveaxis(y.detach().cpu().numpy(), 0, -1)
            y = (y * 255).astype('uint8')
            image = Image.fromarray(y)
            # encode the image to the string for the request
            buffered = BytesIO()
            image.save(buffered, format='JPEG')
            img_encode = base64.b64encode(buffered.getvalue()).decode('utf-8')
            response.append(img_encode)
        if trace:
            for i, img_encode in enumerate(response):
                print(f'send({i}) => {img_encode}')
        return response
    except Exception as ex:
        print('Error occur in script generating!\n', ex)
        raise ChildProcessError(ex)
