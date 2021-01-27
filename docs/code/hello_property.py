import hashlib


class Student(object):

    def __init__(self, password=None):
        self.__password = password

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = hashlib.new('md5', value.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    stu = Student()
    stu.password = '110'
    print(stu.password)