from bottle import route, run, static_file, redirect, response, template
import hashlib
import psycopg2
import cgi
import random
import string
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

@route('/foorum')
def foorum_html():
    return static_file('foorum.html', root='./statics/')

@route('/register')
def register_html():
    return static_file('register.html', root='./statics/')




if __name__ == '__main__':
    run(host='localhost', port=8095, debug=True)

