import os
from flask import Flask, request, jsonify, json, send_file
from flask_redis import FlaskRedis

UPLOAD_FOLDER = '/Users/boris.dergachov/Uploads'
ALLOWED_EXTENSIONS = set(['tar'])

app = Flask(__name__)
redis_store = FlaskRedis(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0


serials_cache = set()


def imageToJson(path: str):
    import base64
    buffer = None
    with(open(path, 'rb')) as file:
        buffer = base64.b64encode(file.read())
        file.close()
    b64buffer = {'b64': buffer.decode('ascii')}
    return b64buffer


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/storage/get_m', methods=['GET'])
def storage_get_m():
    img_path = request.args.get('path_uid')
    # TODO: return placeholder if image not found
    # if img_path is None:
    #     return
    filename = 'tars/' + img_path + '/m.jpg'
    return send_file(filename, mimetype='image/jpg')


def api_uid_to_img_id(img_id : str):
    if img_id is None:
        return str()
    response = redis_store.hscan('uid_to_img_id', cursor=0, match=img_id)
    if (len(response[1]) == 0):
        return str()
    for key, value in response[1].items():
        return value


@app.route('/api/get_jsons', methods=['GET'])
def api_get_jsons():
    response = redis_store.hscan('uid_to_json', cursor=0)
    jsons = list()
    for key, value in response[1].items():
        key = key.decode('utf-8')
        value = json.loads(value.decode('utf-8'))
        img_id = api_uid_to_img_id(key).decode('utf-8')
        jsons.append({
            'uid' : key,
            'json' : value,
            'm' : img_id
        })
    return json.dumps(jsons, sort_keys=False, indent=4)


@app.route('/api/uid_to_json', methods=['GET'])
def api_uid_to_json():
    uid = request.args.get('uid')
    if uid is None:
        return jsonify (
            error_code = -1,
            error_msg = "No uid arg"
        )
    response = redis_store.hscan('uid_to_json', cursor=0, match=uid)
    if len(response[1]) == 0:
        return jsonify (
            error_code = -1,
            error_msg = "uid not found in cache"
        )
    return json.dumps(response[1], sort_keys=False, indent=4)


@app.route('/api/serial_to_uid', methods=['GET'])
def api_serial_to_uid():
    serial = request.args.get('serial')
    if serial is None:
        return jsonify (
            error_code = -1,
            error_msg = "No serial arg"
        )
    return "{}"


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
def api_get_penalties():
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
        for r, d, f in os.walk(root_dir):
            for folder in d:
                if counter == id:
                    json_file = os.path.join(r, folder, "prizma.json")
                    image_file = os.path.join(r, folder, "m.jpg")
                    # encoded base64 str
                    b64str = imageToJson(path=image_file)
                    with open(json_file, encoding='utf-8') as f:
                        json_data = json.load(f)
                    json_data['picture'] = b64str
                    return json.dumps(json_data, sort_keys=False, indent=4)
                counter = counter + 1
    return jsonify(
        error_code=-1,
        error_msg="Not found"
    )


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="10.0.0.61");
