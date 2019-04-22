import os
from flask import Flask, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
import zeroPy

UPLOAD_FOLDER = '/Users/boris.dergachov/Uploads'
ALLOWED_EXTENSIONS = set(['tar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
client = zeroPy.apiClient()

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
        if c == None
            return jsonify(
                error_code = -1
                error_msg = "None object"
            )
        return jsonify(
            blocks=c.blocks,
            transactions=c.transactions,
            user_data=c.binary
        )

if __name__ == '__main__':
    client._handler.connect("10.0.0.27", 38100)
    pub_key = b'1111111111111111111111111111111111111111111111111111111111111111'
    client.send_info(pub_key)
    app.run(host="127.0.0.1");
