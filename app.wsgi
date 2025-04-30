from bottle import route, run, static_file, redirect, response, template, request
import hashlib
import psycopg2
import cgi
import random
import string
import bottle
from beaker.middleware import SessionMiddleware


@route('/')
def index():
    return static_file('index.html', root='./statics/')

@route('/styles.css')
def style_css(): 
    return static_file('styles.css', root='./statics/')

@route('/kuningpuuton')
def kuningpuuton_html():
    return static_file('kuningpuuton.html', root='./statics/')

@route('/habeagaam')
def habeagaam_html():
    return static_file('habeagaam.html', root='./statics/')

@route('/linnutapik')
def linnutapik_html():
    return static_file('linnutapik.html', root='./statics/')

@route('/kuningboa')
def kuningboa_html():
    return static_file('kuningboa.html', root='./statics/')

@route('/PWForm')
def PWForm_html():
    return static_file('PWForm.html', root='./statics/')

@route('/foorum')
def foorum_html():
    return static_file('foorum.html', root='./statics/')

@route('/register')
def register_html():
    return static_file('register.html', root='./statics/')

@route('/about')
def about_html():
    return static_file('about.html', root='./statics/')

@route('/account')
def account_html():
    return template('./statics/account.html', session= request.environ['beaker.session'])  

@route('/login')
def login_html():
    return static_file('login.html', root='./statics/')

@route('/loginpost', method=['POST'])
def loginpost():
    form = cgi.FieldStorage(fp=request.environ['wsgi.input'], environ=request.environ, keep_blank_values=1)
    username = form.getfirst('username')
    password = form.getfirst('password')

    result = check_credentials(username, password)

    if result == "OK":
        request.environ['beaker.session']['username'] = username
        redirect("/")
    else:
        return "Vale Kasutajanimi või Parool"

def check_credentials(username, password):
    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if result:
            stored_password = result[0]
            salt = stored_password[:2]
            stored_password=stored_password[2:]
            crypted = hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()

            if crypted == stored_password:
                return "OK"
            else:
                return "ERROR 1"
        else:
            return "ERROR 2"

    except Exception as e:
        print(f"Andmebaasi viga: {e}")
        return "ERROR"

    finally:
        if conn:
            cur.close()
            conn.close()

@route('/logout')
def logout():
    request.environ['beaker.session'].delete()
    redirect('/')
    
application = bottle.default_app()

# Enable Beaker sessions
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600,
    'session.data_dir': './session',
    'session.auto': True
}
application = SessionMiddleware(application, session_opts)


if __name__ == '__main__':
    run(app=application,host='localhost', port=8095, debug=True)

