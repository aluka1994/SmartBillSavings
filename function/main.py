""" This function handles messages posted to a pubsub topic - ocr by processing
    image file url and storing ocr results to database. The message must be a JSON encoded
    dictionary with fields:
    fileUrl - image file url which needs to be processed
    userId - userId of
    The dictionary may have other fields, which will be ignored.
"""

import json
import os
import sqlalchemy
from google.cloud import storage
from datetime import datetime
from os.path import normpath, basename

from googleapiclient.discovery import build
import requests
from io import BytesIO
from PIL import Image
import base64
from google.cloud import pubsub
import logging

from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
# from google.cloud import error_reporting
# # from google.cloud import logging
# import google.cloud.logging
#
# logging_client = google.cloud.logging.Client(project="gae-cloud-asu")
# logging_client.setup_logging()
# log_name = 'my-log'
# logger = logging_client.logger(log_name)
import google.cloud.logging as cloud_logging
from google.cloud import logging
publisher = pubsub.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

cloud_client = cloud_logging.Client()
log_name = 'cloudfunctions.googleapis.com%2Fcloud-functions'
cloud_logger = cloud_client.logger(log_name)

# client = error_reporting.Client()

db_user = "master"
db_password = "46LyfcwwxCK3dDJq"
db_name = "billing"
db_connection_name = "gae-cloud-asu:us-west4"

# This is for Postgres, datait's similar for MySQL
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@/{db_name}?host=/cloudsql/{db_connection_name}'

# This must be set, determine which is best for you
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CLOUD_STORAGE_BUCKET = "gae-cloud-asu.appspot.com"


# db = sqlalchemy.create_engine(
#     sqlalchemy.engine.url.URL(
#         drivername="mysql",
#         username="master",
#         password="46LyfcwwxCK3dDJq",
#         database="billing",
#         query={"unix_socket": "/cloudsql/{}".format('gae-cloud-asu:us-west4')},
#     ),
# )


class userImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(100), nullable=False)
    imageUrl = db.Column(db.String(1000), nullable=False)
    imageDate = db.Column(db.DateTime, default=datetime.utcnow)
    notify = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'userImage %r %r %r>' % (self.imageName, self.imageUrl, self.notify)


def get_actual_image(image_path):
    if image_path.startswith('https'):
        path = requests.get(image_path, stream=True).raw
    else:
        path = image_path
    return path


def _get_image_bytes_png(image_path):
    image_path = get_actual_image(image_path)
    with BytesIO() as output:
        with Image.open(image_path) as img:
            if not img.mode == 'RGB':
                img = img.convert('RGB')
            img.save(output, 'JPEG')
        data = base64.b64encode(output.getvalue()).decode('utf-8')
    return data


def _get_image_bytes_jpg(image_path):
    image_path = get_actual_image(image_path)
    with BytesIO() as output:
        with Image.open(image_path) as img:
            img.save(output, 'JPEG')
        data = base64.b64encode(output.getvalue()).decode('utf-8')
    return data


def _get_image_bytes(image_path):
    if '.png' in image_path:
        return _get_image_bytes_png(image_path)
    else:
        return _get_image_bytes_jpg(image_path)


def get_ocr_tokens(url):
    APIKEY = "AIzaSyAMm_XI16PEkoikzR5LeXffHbQz132FZwg"
    vision_service = build("vision", "v1", developerKey=APIKEY)
    request = vision_service.images().annotate(body={
        'requests': [{
            'image': {
                'content': _get_image_bytes(url)
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                # 'maxResults': 15,
            }]
        }],
    })
    responses = request.execute(num_retries=5)
    tokens = []
    if 'textAnnotations' not in responses['responses'][0]:
        print("Either no OCR tokens detected by Google Cloud Vision or "
              "the request to Google Cloud Vision failed. "
              "Predicting without tokens.")
        print(responses)
        return []
    result = responses['responses'][0]['textAnnotations'][0]['description']
    '''
    for token in responses['responses'][0]['textAnnotations'][1:]:
      print(token['description'])
      ty.append(token['description'])
      tokens += token['description'].split('\n')
    print(ty)
    '''
    return result


def get_file(url):
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob('bills/' + url)
    full_path = os.path.join('/tmp/', url)
    blob.download_to_filename(full_path)
    return full_path


def parse_message(event, context):
    """ Process a pubsub message
    """
    message = base64.b64decode(event['data'])
    print(message)
    p = json.loads(message)
    print(p)
    # logging.warning("event: ", event)
    # logger.log_text("event: ", event)
    # envelope = json.loads(request.data.decode('utf-8'))
    # payload = base64.b64decode(envelope['message']['imPath'])
    print(event)
    message_data = base64.b64decode(event['data'])
    print(message_data)
    print("new")
    print(message_data.decode('utf-8'))
    # logging.warning("message_data: ", message_data)
    # logger.log_text("message_data: ", message_data)
    message = json.loads(message_data)
    # logger.log_text("message: ", message)

    file_url = message['fileUrl']
    user_id = message['userId']
    # logger.log_text("file_url: ", file_url)
    # logger.log_text("user_id: ", file_url)
    #
    # logger.log_text("staring to get file")
    file_path = get_file(file_url)
    # logger.log_text(file_path)
    data = ""
    data = get_ocr_tokens(file_path)
    # logger.log_text("data processed")
    # logger.log_text("data: ", data)
    base_file_name = basename(normpath(file_url))
    # logger.log_text("base file name: ", base_file_name)
    image_user = userImage(imageName=base_file_name, imageUrl=str(file_url), content=data, timage=user_id)
    try:
        db.session.add(image_user)
        db.session.commit()
    except RuntimeError:
        print("error")
        # client.report_exception()
