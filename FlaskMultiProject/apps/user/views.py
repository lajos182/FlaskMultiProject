
from flask import Blueprint, redirect, url_for, request, render_template, Response, session

from .models import User

user_blue = Blueprint('user_blue', __name__)

'''
1)路由传参,格式<converter:variable_name>
2)converter类型：
    string 接收任何没有斜杠('/')的文件(默认)
    int    接收整型
    float  接收浮点型
    path   接收路径, 可接收斜线('/')
    uuid   接收uuid字符, 唯一码, 一种生成规则
    any    可以同时指定多种路径, 进行限定
3)同一个视图函数, 可以复用, 添加多个装饰器
4)默认支持GET, HEAD, OPTIONS, 如果需要支持其他请求, 需要手动注册, 添加额外的参数methods
'''

@user_blue.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    return f'Hello, 我是用户页面！'

@user_blue.route('/<int:id>/')
def users(id):
    print(id)
    print(type(id))
    return 'Users API'

@user_blue.route('/getinfo/<string:token>/')
@user_blue.route('/gettoken/<int:token>/')
def get_info(token):
    print(token)
    print(type(token))
    return 'Get Info'

@user_blue.route('/getpath/<path:address>/')
def get_path(address):
    print(address)
    print(type(address))
    return 'Get Path'

@user_blue.route('/getuuid/<uuid:uu>/')
def get_uuid(uu):
    print(uu)
    print(type(uu))
    return 'Get uuid'

@user_blue.route('/getany/<any(a,b,c):an>/')
def get_any(an):
    print(an)
    print(type(an))
    return 'Get Any'

@user_blue.route('/redirect/')
def red():
    # 跳转
    # return redirect('/')
    # 反向解析
    # return redirect(url_for('user_blue.index'))
    # 反向解析并传参
    return redirect(url_for('index_blue.get_any', an='a'))

@user_blue.route('/getrequest/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_request():
    print(request.host)
    print(request.url)
    if request.method == 'GET':
        return f'GET success : {request.remote_addr}'
    elif request.method == 'POST':
        return 'POST success'
    else:
        return f'{request.method} Not Support'

@user_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        response = Response(f'{username}登录成功')
        # response.set_cookie('username', username)
        session['username'] = username
        session['password'] = '110'
        return response

@user_blue.route('/mine/')
def mine():
    # username = request.cookies.get('username')
    username = session.get('username')
    print(session)
    print(type(session))
    return f'{username}, 欢迎登录！'

@user_blue.route('/students/')
def students():
    student_list = [f'学生-{i}' for i in range(10)]
    return render_template('students.html', student_list=student_list, a=5, b=7)

@user_blue.route('/user_register/')
def user_register():
    users = [f'小白{i}' for i in range(10)]
    return render_template('user/user_register.html', title='用户注册', users=users, msg='lajos is a handsome boy')