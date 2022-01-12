import logging

logger = logging.getLogger('Dash Model')
logging.basicConfig(format='[ %(name)s API ] %(asctime)s %(message)s',level=logging.INFO)

import json

from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
model_url = os.getenv('model_url')

client = BackendApplicationClient(client_id=client_id)


def transformres(res):
    logging.info(">" * 66)
    logging.info("transformres")
    logging.info(res)
    if not "response" in res :
        logging.error("no response in res")
        return []

    if not "predictions" in res["response"] :
        logging.error("No predictions in response")
        return []

    predictions = res["response"]["predictions"]

    labels = [label.split('_')[-1]  for label in predictions if len(label.split('_')) > 2 ]
    probas = [predictions[f"pred_label_{label}"] for label in labels]
    
    normedPreds = [{"name":name, "similarity":proba} for name, proba in zip(labels, probas)]

    logging.info("<" * 66)
    return normedPreds


def send(text):
    logging.info(">" * 66)
    logging.info("send")
    try:
        predict_url = f"{model_url}/predict"

        payload = json.dumps({
            "text": text
        })
        headers = {'Content-Type': 'application/json'}

        logging.info(payload)
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(
            token_url=
            'https://accounts.prevision.io/auth/realms/prevision.io/protocol/openid-connect/token',
            client_id=client_id,
            client_secret=client_secret)

        prediction = oauth.post(predict_url, headers=headers, data=payload)
        res = prediction
        data=res.json()
        logging.info(data)
        pred = transformres(data)
        logging.info("<" * 66)
        return pred
    except ConnectionError:
        logging.error("Cannot call model")
        return {}


def predict_query(query):
    logging.info(">" * 66)
    logging.info("Prediction over a file")
    p = send(query)
    logging.info("<" * 66)
    return {"predictions": p}

