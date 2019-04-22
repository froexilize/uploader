import os
import time
from threading import Thread
from flask import Flask, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
import zeroPy

UPLOAD_FOLDER = '/Users/boris.dergachov/Uploads'
ALLOWED_EXTENSIONS = set(['tar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/', methods=['GET'])
def api_call():
    if request.method == 'GET':
        return '''
<!doctype html>
<title>API call</title>
<h1>API call</h1>
'''

@app.route('/api/get_counters', methods=['GET'])
def api_get_counters():
    if request.method == 'GET':
        c = client.get_counters()
        if c == None:
            return jsonify(
                error_code = -1,
                error_msg = "None object"
            )
        return jsonify(
            blocks=c.blocks,
            transactions=c.transactions,
            user_data=c.binary
        )

@app.route('/api/get_penalties', methods=['GET'])
def api_test():
    if request.method == 'GET':
        root_dir = './tars'
        jsons = []
        for r, d, f in os.walk(root_dir):
            for folder in d:
                json_file = os.path.join(r, folder, "prizma.json")
                with open(json_file, encoding='utf-8') as f:
                    data = json.load(f)
                jsons.append(json.dumps(data, sort_keys=False, indent=4))
    return json.dumps(jsons, sort_keys=False, indent=4)

@app.route('/api/get_penalty', methods=['GET'])
def api_get_penalty():
    if request.method == 'GET':
        id = int(request.args.get('id'))
        root_dir = './tars'
        tars_path = []
        counter = int(0)
        for r,d,f in os.walk(root_dir):
            for folder in d:
                if counter == id:
                    json_file = os.path.join(r, folder, "prizma.json")
                    image_file = os.path.join(r, folder, "m.jpg")
                    with open(json_file, encoding='utf-8') as f:
                        json_data = json.load(f)
                    image_data = open(image_file)
                    return json.dumps(json_data, sort_keys=False, indent=4)
                counter = counter + 1
    return jsonify(
        error_code = -1,
        error_msg = "Not found"
    )

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="127.0.0.1");
