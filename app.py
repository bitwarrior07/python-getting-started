import os
import importlib
# import ocr
import json
import wget
import json
import requests
import uuid
import logging

from datetime import date, datetime
from functools import wraps
from flask import Flask, request, jsonify, abort, send_from_directory, send_file

logging.basicConfig(filename='app.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


app = Flask(__name__)

@app.route('/')
def homepage():

    return """
    <h1>Hello World! Welcome to bit_warriors_ooty hacks.</h1>
    """
@app.route('/extract/')
def extract():
    data = {}
    image_url = request.args.get('image_url')
    # recog = request.args.get('type')
    upload_dir = 'uploads/'
    # Create directory 'uploads' if it does not exist
    if not os.path.exists(upload_dir):
        print("Uploads directory created")
        os.makedirs(upload_dir)
    file_name = wget.detect_filename(image_url)
    print(file_name)
    file_path = upload_dir + file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    wget.download(image_url, upload_dir)
    data['_id'] = str(uuid.uuid4())
    data['file_name'] = file_name
    data['file_path'] = file_path
    # data['processed_filepath'] = 'processed/' + file_name
    # OCR
    # OCR API
    payload1 = {'apikey': 'K86475666788957',
                'url': image_url,
                'isOverlayRequired': 'True',
                'OCREngine': '1'}
    payload2 = {'apikey': 'K86475666788957',
                'url': image_url,
                'isOverlayRequired': 'True',
                'OCREngine': '2'}
    data['ocr'] = []
    # data['ocr'].append(
    #     {
    #         "tresh": ocr.ocr(data['file_name'], data['file_path'], 'tresh'),
    #         "blur": ocr.ocr(data['file_name'], data['file_path'], 'blur'),
    #         "engine1": json.loads(ocr.ocr_api(image_url, payload1).text),
    #         "engine2": json.loads(ocr.ocr_api(image_url, payload2).text)
    #     })
    jsonified_data = jsonify(data)
    return jsonified_data

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

