from flask import Flask, request, jsonify, make_response
import datetime
import jwt
from functools import wraps
# jsonify retorna objetos em json ao inves de html
# make_response diz para o navegador ou a API qual é o HTTP basic pedido para login

from db import callLane, callVersion, callEnv, file

# testado com postman/ postman agent
app = Flask("Inchurch API")

# chave secreta pra codificar o token
app.config['SECRET_KEY'] = 'secret_inchurch'


# rota get
# @app.route("/wl/ios/get", methods=['GET'])
# def wl_get():
#     return {"target": "cristovivesp"}
# request do token p multiplas rotas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.args.get('auth')  # http://127.0.0.1:5000/route?auth=exemplodetoken

        if not auth:
            return jsonify({'exception': 'Requer o token'}), 401  # or 403

        try:
            data = (auth, app.config['SECRET_KEY'])
        except:
            return jsonify({'exception': 'Token de autenticação inválido'}), 401  # or 403

        return f(*args, **kwargs)

    return decorated


@app.route('/test')
@token_required
def test():
    return {"token": "ENTROU COM SUCESSO"}


# rota post
# rota protegida, apenas com autenticação
@app.route("/inchurch/rest/api/1.0/fastlane", methods=['GET'])
@token_required
def fastlane():

    if request.method == 'GET':
        if "lane" not in file:
            return {"status": 400, "message": "Parâmetro 'lane' está faltando."}

        if "version" not in file:
            return {"status": 400, "message": "Parâmetro 'version' está faltando."}

        if "env" not in file:
            return {"status": 400, "message": "Parâmetro 'env' está faltando."}

        lane_param = callLane()
        version_param = callVersion()
        env_param = callEnv()

        return responseMessage(200, "Comando gerado", "fastlane",
                               f'bundle exec fastlane {lane_param} version:{version_param} --env {env_param}')


def responseMessage(status, message, label, content):
    response = {}
    response["status"] = status
    response["message"] = message

    if label and content:
        response[label] = content

    return response


@app.route('/inchurch/rest/api/1.0/auth')
def auth_token():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Verificado!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    # return make_response({'Nao foi possivel verificar': 401}, {"Auto_WL": "requer Auth"})


if __name__ == '__main__':
    app.run(debug=True)
