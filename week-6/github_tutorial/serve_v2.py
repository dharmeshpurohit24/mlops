import os
import json

import time
from datetime import datetime
from pathlib import Path
import logging

import mlflow
from flask import Flask, request, jsonify

MODEL_VERSION = os.getenv('MODEL_VERSION',"1.0")
MODEL_URI = os.getenv('MODEL_URI',"models:/trip_duration@staging")

mlflow.set_tracking_uri("http://localhost:5000")
model = mlflow.pyfunc.load_model(MODEL_URI)

logger = logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


def prepare_features(ride):
    features = {}
    features['PULocationID'] = str(ride['PULocationID'])
    features['DOLocationID'] = str(ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict([features])
    return float(preds[0])


def log_result(result):
    # IMPORTANT:
    # Saving to files is a very bad practice. Don't do it
    # This is just an illustration - to make the workshop simpler
    # In practice, use logstash, kafka, kinesis, mongo, etc for that

    try:
        now = datetime.now()

        date_now = now.strftime('%Y-%m-%d')
        time_now = int(time.mktime(now.timetuple()))

        path = Path('logs') / date_now / f'{time_now}.json'
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open('wt', encoding='utf-8') as f_out:
            json.dump(result, f_out)

    except (OSError, IOError) as err:
        logger.error("Failed to write log file: %s", err)

    except (TypeError, ValueError) as err:
        logger.error("Failed to serialize result to JSON: %s", err)

    except Exception:
        logger.exception("Unexpected error while logging result")



app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    body = request.get_json()
    ride = body['ride']
    ride_id = body['ride_id']

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'prediction': {
            'duration': pred,
        },
        'ride_id': ride_id,
        'model_version': MODEL_VERSION
    }

    log_result(result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)