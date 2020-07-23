from flask import Flask, jsonify, abort, request
from flasgger import swag_from
import json
import os
import time
import logging
import uuid
import zipfile

from . import api
from ai import *
from config import apiversion


@api.route('/api/ai/predict', methods=['POST'])
@swag_from('predict.yaml')
def analyze_image():
    # prepare api
    if not request.json:
        abort(400)
    if 'healthcheck' in request.json:
        return ""
    try:
        dirPath = hello(request.json['path'])

        return jsonify({'fieldA': dirPath}), 200, {"api_version": apiversion}

    except Exception:
        error_code = str(uuid.uuid1())
        properties = {
            'custom_dimensions': {
                'error_code': error_code,
                'category': 'ai'
            }
        }
        logging.exception('Captured an exception.', extra=properties)
        return f'error_code:{error_code}', 500, {"error_code": error_code}
