from flask import Flask, jsonify, make_response, request
import requests
from flask_cors import CORS
import boto3
import socket

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    response = make_response(
        jsonify(
            {"message": "Hello from app"}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getTag', methods=['GET'])
@app.route('/getTag/', methods=['GET'])
def get_tag():
    tag = request.args.get('tag')

    instance_id = (requests.get("http://169.254.169.254/latest/meta-data/instance-id")).text


    ec2 = boto3.resource('ec2', region_name="us-east-1")
    ec2instance = ec2.Instance(instance_id)
    host = socket.gethostname();
    server = {"name": "Tag not found!", "host": host}
    found = False

    for tags in ec2instance.tags:
        print(tags)
        if tag in tags['Key']:
            server = {"name": tags['Value'], "host": host}
            found = True
            break

    codigo = 200 if found else 404

    response = make_response(
        jsonify(server),
        codigo,
    )
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)