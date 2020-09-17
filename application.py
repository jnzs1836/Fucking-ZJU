from flask import Flask, request, render_template, make_response, session, redirect, url_for
from datetime import datetime, timedelta
import pprint
application = Flask(__name__)
application.secret_key = b'_5#ysdsadf2LdsfdsF4Q8z\n\xec]/'



@application.route('/')
def hello_world():
    return 'Hello World!'


users = [
    {
        'access_key': "qiuqiu",
        "username": "djcheng",
        'student_name': '陈丹箐',
    },
    {
        'access_key': "ohhyun",
        'username': "cbzheng",
        'student_name': '郑成博',
    },
    {
        'access_key': "orange",
        "username": "yjzheng",
        'student_name': '郑宇洁',
    },
    {
        'access_key': "father",
        "username": "gdwu",
        'student_name': '吴冠德',
    },
    
    {
        'access_key': "anyone",
        "username": "hren",
        'student_name': '任贺',
    },
    {
        'access_key': "noone",
        "username": "renmei",
        'student_name':'梅仞',
    }
]



def valid_login(access_key):
    keys = list(map(lambda x: x['access_key'], users))
    print(keys)
    if access_key in keys:
        return True
    else:
        return False
    
def log_the_user_in(access_key):
    user = list(filter(lambda x: x["access_key"]==access_key, users))[0]
    session['username'] = user['access_key']
    session['student_name'] = user['student_name']
    resp = make_response(build_blue_code(user['student_name']))
    resp.set_cookie('student_name', user['student_name'])
    resp.set_cookie("username", user['username'])
    return redirect(url_for('blue_code'))

@application.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        
        pprint.pprint(request.form)
        if valid_login(request.form['accessKey']):
            
            return log_the_user_in(request.form['accessKey'])
        else:
            error = 'Invalid username/password'
    return render_template("login.html")


def build_blue_code(student_name):
    now = datetime.now()
    def format_time(timestamp):
        return timestamp.strftime("%Y-%m-%d")
    valid_time_str = "有效期：" + format_time(now) + " - " +format_time(now + timedelta(days=1))
    return render_template('zju-blue-code.html', student_name=student_name, valid_time=valid_time_str)

@application.route('/blue_code')
def blue_code():
    if "username" in session:
        return build_blue_code(session['student_name'])    
    else:
        return render_template("login.html")

if __name__ == '__main__':
    application.debug = True
    application.run()
