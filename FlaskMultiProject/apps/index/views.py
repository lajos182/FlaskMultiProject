
from flask import Blueprint, render_template, request, make_response, Response, abort

# from .models import User

index_blue = Blueprint('index_blue', __name__)

@index_blue.route('/')
def index():
    return render_template('index.html')

@index_blue.route('/sendrequest/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def send_request():
    # ImmutableMultiDict([('user', 'lajos'), ('password', '1234'), ('password', '123444')])
    print(request.args)
    print(type(request.args))

    print(request.form)
    print(type(request.form))

    print(request.headers)
    return 'send success'

@index_blue.route('/getresponse/')
def get_response():
    # 可以直接使用元组
    # return 'Get response', 400
    # result = render_template('index.html')
    # print(result)
    # print(type(result))
    # return result
    # response = make_response('<h1>获取响应！</h1>')
    # print(response)
    # print(type(response))
    abort(404)
    response = Response('自己造一个response')
    return response

# 异常捕获
@index_blue.errorhandler(404)
def handle_error(error):
    print(error)
    print(type(error))
    return 'What?'