import random

from flask import Blueprint, redirect, url_for, request, render_template, Response, session, flash
from flask_mail import Message
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, Student, Cat, Dog, Customer, Address
from ..extensions import db, cache, mail

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

@user_blue.route('/addstudent/')
def add_student():
    student = Student()
    student.name = f'小明{random.randrange(10000)}'
    db.session.add(student)
    db.session.commit()
    return 'Add Success'

@user_blue.route('/addstudents/')
def add_students():
    students = []
    for i in range(5):
        student = Student()
        student.name = f'小花{random.randrange(10000)}'
        students.append(student)
    db.session.add_all(students)
    db.session.commit()
    return 'Add All Success'

@user_blue.route('/getstudent/<int:id>/')
def get_student(id):
    # student = Student.query.first()
    # 没有last方法
    # student = Student.query.last()
    # student = Student.query.get_or_404(22)
    student = Student.query.get(id)
    print(student)
    return 'Get Student Success'

@user_blue.route('/getstudents/')
def get_students():
    students = Student.query.all()
    for student in students:
        print(student.name)
    return render_template('user/student_list.html', students=students)

@user_blue.route('/delstudent/')
def delete_student():
    student = Student.query.first()
    db.session.delete(student)
    db.session.commit()
    return 'Delete Student Success'

@user_blue.route('/updatestudent/')
def update_student():
    student = Student.query.first()
    student.name = 'lajos'
    db.session.add(student)
    db.session.commit()
    return 'Update Student Success'

@user_blue.route('/redir/')
def redir():
    url = url_for('user_blue.get_student', id=1)
    return url

@user_blue.route('/addcat/')
def add_cat():
    cat = Cat()
    cat.name = '加菲猫'
    cat.eat = 'bone'
    db.session.add(cat)
    db.session.commit()
    return 'Add Cat Success'

@user_blue.route('/adddog/')
def add_dog():
    dog = Dog()
    dog.name = '金毛'
    dog.habit = 'shower'
    db.session.add(dog)
    db.session.commit()
    return 'Add Dog Success'

@user_blue.route('/adddogs/')
def add_dogs():
    dogs = []
    for i in range(50):
        dog = Dog()
        dog.name = f'二哈{i}'
        dog.habit = i
        dogs.append(dog)
    db.session.add_all(dogs)
    db.session.commit()
    return 'Add Dogs Success'

@user_blue.route('/getcats/')
def get_cats():
    # cats = Cat.query.filter(Cat.id.__eq__(2)).all()
    # cats = Cat.query.filter(Cat.id == 2)
    # cats = Cat.query.filter(Cat.id.in_([2, 3]))
    # cats = Cat.query.filter(Cat.id.__lt__(5)).all()
    # cats = Cat.query.order_by(Cat.id.desc()).limit(2).offset(2)
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 2, type=int)
    cats = Cat.query.offset(size * (page - 1)).limit(size)
    print(type(cats))
    return render_template('user/cats.html', title='cats', cats=cats)

@user_blue.route('/getdogs/')
def get_dogs():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    dogs = Dog.query.offset(size * (page - 1)).limit(size)
    print(type(dogs))
    return render_template('user/dogs.html', title='dogs', dogs=dogs)

@user_blue.route('/getdogswithpage/')
def get_dogs_with_page():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    # dogs = Dog.query.paginate(page=page, per_page=size).items
    pagination = Dog.query.paginate(page=page, per_page=size)
    return render_template('user/dogs.html', title='dogs', pagination=pagination, size=size)

@user_blue.route('/getcatsfilterby/')
def get_cats_filter_by():
    cats = Cat.query.filter_by(id=5)
    return render_template('user/cats.html', cats=cats)

@user_blue.route('/addcustomer/')
def add_customer():
    customers = []
    for i in range(10):
        customer = Customer()
        customer.name = f'剁手党{random.randrange(10000)}'
        customers.append(customer)
    db.session.add_all(customers)
    db.session.commit()
    return 'Add Customer Success'

@user_blue.route('/addaddress/')
def add_address():
    addresses = []
    customers = Customer.query.all()
    for customer in customers:
        for i in range(random.randrange(10)):
            address = Address()
            address.customer_id = customer.id
            address.position = f'香格里拉{random.randrange(10000)}'
            addresses.append(address)
    db.session.add_all(addresses)
    db.session.commit()
    return 'Add Adress Success'

@user_blue.route('/getcustomer/')
def get_customer():
    id = request.args.get('id', type=int, default=1)
    address = Address.query.get_or_404(id)
    customer = Customer.query.get(address.customer_id)
    return customer.name

@user_blue.route('/getaddresses/')
def get_addresses():
    id = request.args.get('id', type=int, default=1)
    customer = Customer.query.get_or_404(id)
    # addresses = Address.query.filter_by(customer_id=customer.id)
    addresses = customer.addresses
    print(addresses, '----------')
    print(type(addresses), '----------')
    return render_template('user/address_list.html', addresses=addresses)

@user_blue.route('/getaddresswithcondition/')
@cache.cached(timeout=60)
def get_address_with_condition():
    # addresses = Address.query.filter(Address.customer_id.__eq__(1)).filter(Address.position.endswith('4'))
    # addresses = Address.query.filter(and_(Address.customer_id.__eq__(1), Address.position.endswith('4')))
    addresses = Address.query.filter(or_(Address.customer_id.__eq__(1), Address.position.endswith('4')))
    print('从数据库中获取数据')
    return render_template('user/address_list.html', addresses=addresses)


@user_blue.route('/student/register/', methods=['GET', 'POST'])
def student_register():
    if request.method == 'GET':
        return render_template('user/student_register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        student = Student()
        student.username = username
        student.password = password
        db.session.add(student)
        db.session.commit()
        return 'Register Success'

@user_blue.route('/student/login/', methods=['GET', 'POST'])
def student_login():
    if request.method == 'GET':
        return render_template('user/student_login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        student = Student.query.filter(Student.username.__eq__(username)).first()
        if student and student.check_password(password):
            return 'Login Success'
        flash(message='用户名或密码错误')
        return redirect(url_for('user_blue.student_login'))

@user_blue.route('/sendmail/')
def send_mail():
    msg = Message(
        subject='Flask Mail',
        recipients=['', ]
    )
    msg.body = '哈哈。。。。'
    msg.html = '<h1></h1>'
    mail.send(message=msg)
    return 'Send Success'