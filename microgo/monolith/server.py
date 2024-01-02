from flask import Flask, request, make_response, send_file
import logging

from instantiation import app_log, authenticator, file_access

from modules.errors import Error
from middleware.authenticate_route import authentication
from controllers import upload_controller, download_controller

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)




def log_route_name(app):
    @app.before_request
    def log_route():
        app_log(f'{request.remote_addr} make a {request.method} request on route `{request.path}`', 'info', tag='route access')

    return app
app = log_route_name(app)

@app.route('/')
def index():
    return 'hello world', 200

@app.route('/login')
def login():
    if not request.authorization:
        return {"message": "Authorization header not found"}, 401
    
    signed_token = authenticator.sign_user(request.authorization.username, request.authorization.password)
    if not isinstance(signed_token, Error):
        resp = make_response({'message': 'Login sucess', 'token': signed_token})
        resp.headers['Authorization'] = 'Bearer ' + signed_token
        resp.status_code = 200

    else:
        resp = make_response({'message': signed_token.message})
        resp.status_code = 401

    return resp

@app.route('/upload', methods=['POST'])
def upload_ctrl():
    signature = authentication(request, authenticator)
    if isinstance(signature, Error):
        return signature.message, 400
    
    fs_id = upload_controller(signature, request)
    if isinstance(fs_id, Error):
        return fs_id.message, 500
    return {'fs_id': fs_id}, 201

@app.route('/download', methods=['POST'])
def download_ctrl():
    signature = authentication(request, authenticator)
    if isinstance(signature, Error):
        return signature.message, 400
    fs_id = request.get_json().get('fs_id')
    resp = download_controller(fs_id, signature)
    if isinstance(resp, Error):
        if resp.code == 'fs_error':
            return resp.message, 400
        else:
            return resp.message, 401
    return send_file(resp[1], download_name=resp[0])


@app.route('/img_collection', methods=['GET'])
def img_collection():
    signature = authentication(request, authenticator)
    if isinstance(signature, Error):
        return signature.message, 400

    fs_id_list = file_access.list_imgs(signature)
    return fs_id_list


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)