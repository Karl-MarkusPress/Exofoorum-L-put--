from bottle import route, run, static_file, redirect, response, template, request
import hashlib
import mimetypes
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

#TEHA SQL paring POST tabelist, ning tulemus anda foorum html lehel ette. TEMPLATE peab naitama tabelina valja postitused !!!!!!
@route('/foorum')
def foorum_html():
    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        cur.execute("SELECT P.*, I.title, I.id AS Image_Id, U.username FROM posts P LEFT JOIN images I On P.ID=I.postid INNER JOIN USERS U on P.CreatorID=U.id ORDER BY P.id DESC")
        posts = cur.fetchall()

        cur.execute("SELECT C.*, I.title, I.id AS Image_Id, U.username FROM Comments C LEFT JOIN images I On C.ID=I.Commentsid INNER JOIN USERS U on C.CreatorID=U.id ORDER BY C.id DESC")
        temp = cur.fetchall()
        Comments={}
        for row in temp:
            if row [3] not in Comments:
                Comments[row[3]]=[]
            Comments[row[3]].append(row)

    except Exception as e:
        print(f"Andmebaasi viga: {e}")
        return "ERROR"

    finally:
        if conn:
            cur.close()
            conn.close()
    return template('./statics/foorum.html', posts=posts, session= request.environ['beaker.session'], Comments=Comments)

@route('/image')
def Pilt_html():
    imageID = request.params.get('imageID')
    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        cur.execute("SELECT title,contents FROM images WHERE id=%s", (imageID,))
        image = cur.fetchone()
        if not image:
            return "Sellist pilti ei eksisteeri"



        bytes = image[1][:]
        response.set_header('Content-type', mimetypes.guess_type(image[0])[0] or "application/octet-stream")
        return bytes

    except Exception as e:
        print(f"Andmebaasi viga: {e}")
        return "ERROR"

    finally:
        if conn:
            cur.close()
            conn.close()

@route('/foorumpost', method=['POST'])
def foorumpost():
    
    post_Title = request.params.get('post-title')
    post_text = request.params.get('post-text')

    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        cur.execute("INSERT INTO posts (CreatorID, Title, Comments) VALUES (%s, %s, %s) returning id", (1, post_Title, post_text))
        postID=cur.fetchone()[0]
        uploadfile = request.files.get('photo')
        if uploadfile and uploadfile.filename:
            uploadfiledata = uploadfile.file.read()

            cur.execute("""INSERT INTO images (postid, title, contents) VALUES (%s, %s, %s)""", (postID, uploadfile.filename, psycopg2.Binary(uploadfiledata)))
        redirect("/foorum")
   # except response:
       # raise
    #except Exception as e:
       #print(f"Andmebaasi viga: {e}")
       # return "ERROR"

    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()

@route('/kommenteeri/<post_id>', method=['POST'])
def kommentaar(post_id):
    
    comment_text = request.params.get('comment-text')

    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        cur.execute("INSERT INTO Comments (CreatorID, PostID, Comments) VALUES (%s, %s, %s) returning id", (1, post_id, comment_text))
        CommentID=cur.fetchone()[0]
        uploadfile = request.files.get('photo')
        if uploadfile and uploadfile.filename:
            uploadfiledata = uploadfile.file.read()

            cur.execute("""INSERT INTO images (CommentsID, title, contents) VALUES (%s, %s, %s)""", (CommentID, uploadfile.filename, psycopg2.Binary(uploadfiledata)))
        redirect("/foorum")
   # except response:
       # raise
    #except Exception as e:
       #print(f"Andmebaasi viga: {e}")
       # return "ERROR"

    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()

@route('/register')
def register_html():
    return static_file('register.html', root='./statics/')

@route('/registerpost', method=['POST'])
def registerpost():
    
    username = request.params.get('username')
    password = request.params.get('passsword')
    passwordConfirm = request.params.get('passswordconfirm')

    conn = None
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5433")
        cur = conn.cursor()

        salt= random[2]
        crypted = salt + hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) ", (username, hashpassword))
        redirect("/login")

    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()

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
    'session.cookie_expires': 40000,
    'session.data_dir': './session',
    'session.auto': True
}
application = SessionMiddleware(application, session_opts)


if __name__ == '__main__':
    run(app=application,host='localhost', port=8095, debug=True)

