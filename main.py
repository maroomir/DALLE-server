import os

import metaartserver

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

os.environ['FLASK_APP'] = 'metaartserver'

if __name__ == "__main__":
    dalle_model = os.path.join(MODEL_DIR, '16L_64HD_8H_512I_128T_cc12m_cc3m_3E.pt')
    app = metaartserver.create_app(dalle_path=dalle_model, data_path=DATA_DIR)
    app.run(host='0.0.0.0')
