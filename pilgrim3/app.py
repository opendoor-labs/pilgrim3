#!/usr/bin/env python

import os
import sys
import time
from flask import Flask, Response
from flask.ext.cors import CORS

base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
path = os.path.join(base_path, 'pb')
sys.path.append(os.path.normpath(path))

from google.protobuf.descriptor_pb2 import FileDescriptorSet
from google.protobuf.json_format import MessageToJson

app = Flask(__name__, instance_path=os.path.join(base_path, 'pilgrim3'))
CORS(app)

bundle_path = os.path.join(base_path, 'proto_bundle')
local_path = os.path.join('./', 'proto_bundle')

@app.route('/google/proto-bundle')
def fetchGoogleProtos():
    raw_json = fetchProtoJSON(bundle_path)
    resp = Response(
            response=raw_json,
            status=200,
            mimetype="application/json"
            )
    return resp

@app.route('/local/proto-bundle')
def fetchLocalProtos():
    raw_json = fetchProtoJSON(local_path)
    resp = Response(
            response=raw_json,
            status=200,
            mimetype="application/json"
            )
    return resp

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

def fetchProtoJSON(the_path):
    with open(the_path, 'rb') as f:
        raw_proto = FileDescriptorSet()
        raw_proto.ParseFromString(f.read())
        f.close()

    return MessageToJson(raw_proto)

app.run(port=9151, threaded=True)
