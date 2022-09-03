import os

import metaartserver

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

os.environ['FLASK_APP'] = 'metaartserver'
os.environ['FLASK_ENV'] = 'development'

if __name__ == "__main__":
    dalle_model = os.path.join(MODEL_DIR,
                              '16L_64HD_8H_512I_128T_cc12m_cc3m_3E.pt')
    app = metaartserver.create_app(dalle_path=dalle_model)
    app.run(host=metaartserver.TEST_INTERNAL_SERVER,
            port=metaartserver.TEST_INTERNAL_PORT)
