import werkzeug.exceptions
from flask import Flask, jsonify, request, g, make_response
from flask_cors import CORS
# from flask_restful import Api, Resource
# from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint
from cars_blueprint import cars_bp
from registry_blueprint import registry_bp
from users_blueprint import users_bp
from contract_nou.CarRegistry import CarRegistry
from user_service import *


app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers=['X-New-Token', 'X-Role'])
###########################################################
# SWAGGER_URL = "/swagger"
# API_URL = "/static/swagger.json"
# swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
#     'app_name': 'Access API'
# })
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
############################################################


app.register_blueprint(cars_bp, url_prefix='/cars')
app.register_blueprint(registry_bp, url_prefix='/registry')
app.register_blueprint(users_bp, url_prefix='/users')

car_registry = CarRegistry()
cars_bp.car_registry = car_registry
registry_bp.car_registry = car_registry
###########################################################

'''
/cars/ pentru toata lumea
/registry/ pentru useri
/users/ pentru admini
'''

@app.before_request
def before_request():
    print(request.method)
    if request.method == "OPTIONS":
        return make_response()
    # print(request.headers)
    path = request.path
    print(path)
    if request.method == 'POST' or request.method == 'PUT':
        if request.is_json == False:
            return jsonify({"message": "If the body is present it must be JSON"}), 400
        g.token = ""
        g.userId = 0
    if path.startswith("/registry"):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return jsonify({"message": "No token provided!"}), 401
        g.token = authorization_header[7:]
        g.refresh_token = refresh_token(g.token)
        decoded = decode_and_verify_token(g.refresh_token)
        g.userId = decoded['sub']
        if get_role_by_id(g.userId) != "USER":
            raise CustomException("You don't have permission to access this endpoint!", 403)
    #todo comenteaza asta pentru testare
    # if path.startswith("/users"):
    #     authorization_header = request.headers.get('Authorization')
    #     if not authorization_header:
    #         return jsonify({"message": "No token provided!"}), 401
    #     g.token = authorization_header[7:]
    #     g.refresh_token = refresh_token(g.token)
    #     decoded = decode_and_verify_token(g.refresh_token)
    #     g.userId = decoded['sub']
    #     if get_role_by_id(g.userId) != "ADMIN":
    #         raise CustomException("You don't have permission to access this endpoint!", 403)



@app.after_request
def after_request(response):
    if hasattr(g, 'refresh_token'):
        response.headers['X-New-Token'] = refresh_token(g.refresh_token)
        del g.token
        del g.refresh_token
    return response


@app.errorhandler(Exception)
def handle_custom_exception(error):
    if isinstance(error, CustomException):
        return jsonify({'error': error.get_message()}), error.get_status_code()
    if isinstance(error, werkzeug.exceptions.NotFound):
        return jsonify({'error': "Endpoint Not found"}), 404
    else: #if isinstance(error, ValueError):
        return jsonify({'error': error.args[0]["message"]}), 500

    # print("Eroare :" + str(error))
    # return jsonify({'error': error.args[0]}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token, role = login_user(data['username'], data['password'], )
    g.refresh_token = token
    response = make_response(jsonify({"success": True, "data": "Successfully logged in"}))
    response.status_code = 200
    response.headers['X-Role'] = role
    return response


@app.route('/logout', methods=['POST'])
def logout():
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({"message": "No token provided!"}), 401
    cancel_token(authorization_header[7:])
    return jsonify({"success": True, "data": "Logout succesful"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    data=str(str(datetime.utcnow())+str(data))
    print("Data received"+data)
    with open("registrations.txt", 'a') as file:
        file.write(data + '\n')
    # todo ar trebui sa primesc niste informatii pe care le pastrez, paote mai tarziu le primesc e mail
    return jsonify({"success": True, "data": "Data received"}), 200

@app.route('/refresh', methods=['POST'])
def refresh():
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({"message": "No token provided!"}), 401
    g.token = authorization_header[7:]
    g.refresh_token = refresh_token(g.token)
    g.userId = decode_and_verify_token(g.refresh_token)['sub']
    response= make_response(jsonify({"message": "Token refreshed"}), 200)
    response.headers['X-Role'] = get_role_by_id(g.userId)
    return response

#########################################################

# def print_request_details(request):
#     print("User id: " + str(g.userId))
#     print("Role: " + str(g.role))
#     print("Token: " + str(g.token))
#     print("Path: " + str(request.path))
#     print("Method: " + str(request.method))
#     print("Headers: " + str(request.headers))
#     print("Body: " + str(request.get_json()))
#     print("Query: " + str(request.args))
#     print("Form: " + str(request.form))
#     print("Cookies: " + str(request.cookies))
#     print("Files: " + str(request.files))
#     print("Data: " + str(request.data))
#     print("Endpoint: " + str(request.endpoint))
#     print("Full path: " + str(request.full_path))
#
#     print("Host: " + str(request.host))
#     print("Method: " + str(request.method))
#     print("Path: " + str(request.path))
#     print("Remote addr: " + str(request.remote_addr))
#     print("Scheme: " + str(request.scheme))
#     print("Url: " + str(request.url))
#     print("Base url: " + str(request.base_url))
#     print("Url root: " + str(request.url_root))
#     print("Maxs content length: " + str(request.max_content_length))


if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)
