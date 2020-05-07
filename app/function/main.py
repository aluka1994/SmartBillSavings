# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_pubsub_setup]
import base64
from google.cloud import pubsub_v1
import json
import os


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')



# [START functions_pubsub_subscribe]
#command
#gcloud functions deploy Translate --runtime=python37 --entry-point=subscribe --trigger-topic=ocr --set-env-vars GOOGLE_CLOUD_PROJECT=ccnew-275119
# Triggered from a message on a Cloud Pub/Sub topic.
def subscribe(event, context):
    # Print out the data from Pub/Sub, to prove that it worked
    message = base64.b64decode(event['data'])
    print(message)
    p = json.loads(message)
    print(p)
# [END functions_pubsub_subscribe]