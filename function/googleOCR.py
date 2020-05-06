'''
pip install google-api-python-client
pip install requests
pip install Pillow

'''
from googleapiclient.discovery import build
import requests
from io import BytesIO
from PIL import Image
import base64


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


def _get_ocr_tokens(url):
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


# if __name__ == '__main__':
#     result = _get_ocr_tokens("https://ccnew-275119.ue.r.appspot.com/get_file/8FD7F482-FA07-4212-B789-D613D4BB5302.jpeg")
#     print(result)
