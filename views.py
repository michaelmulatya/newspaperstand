import datetime
import timeit
from functools import wraps
from sqlalchemy import func, or_
from flask import render_template, flash, redirect, url_for, session, request, Blueprint, send_file,jsonify
from passlib.hash import sha256_crypt
from cash import Mpesa
from core import app, db, photos
from core.models import Admin, Orders, Products, ProductLevel, ProductView, Users, Messages, Request
from forms import LoginForm, RegisterForm, MessageForm, OrderForm, UpdateRegisterForm, DeveloperForm, RequestForm
import string
import paypalrestsdk
import requests
import json
import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAIPEPT7GFYD5VOZRQ'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'wanderift'

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)



# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_experimental_option("prefs", {
#   "download.default_directory": "./download/",
#   "download.prompt_for_download": False,
# })
# # driver = webdriver.Chrome(chrome_options=options)
# driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
# params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "./download/"}}
# command_result = driver.execute("send_command", params)

paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": "AerFGosD8Ndp419g717X_eRKaVU8834Jj9HIWAhnpQP7H3uwsVK3XWK7hQngYQFg401nd5KdK0V2INwY",
      "client_secret": "EAEfZ67HRloa4jl_pWKX59_-KXUeXYyiw4gcEVN_DmGzUCjovV1D6pvLn809owy3CQsSIqBCbpCDHvvA" })



core = Blueprint('core',__name__)

#request.base_url
pesa = Mpesa('newspaperstand.herokuapp.com',"174379")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def content_based_filtering(product_id):
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # getting id row
    # data = cur.fetchone()  # get row info
    data = Products.query.filter_by(id = product_id).first()
    # print(data)
    # print(type(data))
    data_cat = data.category # get id category ex shirt
    # print(data_cat)
    # print('Showing result for Product Id: ' + product_id)
    # category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
    category_matched = Products.query.filter_by(category = data_cat)
    print('Total product matched: ' + str(category_matched))
    # cat_product = cur.fetchall()  # get all row
    cat_product = Products.query.filter_by(category= data_cat).all()
    # cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id level info
    # id_level = cur.fetchone()
    id_level = ProductLevel.query.filter_by(id = product_id).first()
    recommend_id = []
    cate_level = ['v_shape', 'polo', 'clean_String', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
                  'chain']
    for product_f in cat_product:
        # cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        # f_level = cur.fetchone()
        f_level = ProductLevel.query.filter_by(id = product_f.id).first()
        match_score = 0
        if f_level.product_id != int(product_id):
            for cat_level in cate_level:

                if getattr(f_level,cat_level) == getattr(id_level,cat_level):
                    match_score += 1
            if match_score == 11:
                recommend_id.append(f_level.product_id)
    print('Total recommendation found: ' + str(recommend_id))
    if recommend_id:
        # cur = mysql.connection.cursor()
        # placeholders = ','.join((str(n) for n in recommend_id))
        # print(placeholders)

        # query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
        # cur.execute(query)
        # recommend_list = cur.fetchall()
        recommend_list = Products.query.filter(Products.id.in_(recommend_id)).all()
        return recommend_list, recommend_id, category_matched, product_id
    else:
        return ''


def format_phone(phone):  # formats all the numbers to the required format
    punct_map = dict.fromkeys(map(ord, string.punctuation))  # removes all punctuation
    number = phone.translate(punct_map)
    number = number.replace(" ","")
    number = number.lstrip("0")
    if number.startswith('254') and len(number)==12:
        return number
    else:
        number = '254'+number
        return number


@app.route('/')
def index():
    form = OrderForm(request.form)
    # Create cursor
    # cur = mysql.connection.cursor()
    # Get message
    values = 'magazines'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # magazines = cur.fetchall()
    magazines = Products.query.filter_by(category = values).order_by(func.random()).limit(4).all()
    values = 'comics'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # comics = cur.fetchall()
    comics = Products.query.filter_by(category = values).order_by(func.random()).limit(4).all()
    values = 'textbooks'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # textbooks = cur.fetchall()
    textbooks = Products.query.filter_by(category = values).order_by(func.random()).limit(4).all()
    values = 'newspapers'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # newspapers = cur.fetchall()
    newspapers = Products.query.filter_by(category = values).order_by(func.random()).limit(4).all()
    # Close Connection
    # cur.close()
    current_time = datetime.datetime.utcnow()

    week_ago = current_time - datetime.timedelta(weeks=2)
    newest = Products.query.filter(Products.date < week_ago).order_by(Products.id.desc()).limit(8).all()

    if 'order' in request.args:
        product_id = request.args['order']
        session['pid']= product_id

        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        product = Products.query.filter_by(id = product_id).all()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, products=product, form=form)

    return render_template('home.html', magazines=magazines, comics=comics, textbooks=textbooks, newspapers=newspapers, newest = newest, form=form)





# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        # cur = mysql.connection.cursor()

        # Get user by username
        # result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
        result = Users.query.filter_by(username = username).first()
        print(result)
        if result:
            # Get stored value
            # data = cur.fetchone()
            password = result.password
            uid = result.id
            name = result.name

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                # cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                Users.query.filter_by(id = uid).update(dict(online = x))
                # online.online = x
                db.session.commit()
                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            # cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        # cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        # cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        Users.query.filter_by(id=uid).update(dict(online=x))
        session.clear()
        db.session.commit()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))




@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobile = form.mobile.data

        # Create Cursor
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO users(name, email, username, password, mobile) VALUES(%s, %s, %s, %s, %s)",
        #             (name, email, username, password, mobile))
        #
        # # Commit cursor
        # mysql.connection.commit()
        #
        # # Close Connection
        # cur.close()
        one = Users(name, email, username,password,mobile, reg_time= datetime.datetime.utcnow(), online= 0,activation= 'yes')
        db.session.add(one)
        db.session.commit()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)





@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Create cursor
        # cur = mysql.connection.cursor()

        # lid name
        # get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
        # l_data = cur.fetchone()
        get_result = Users.query.filter_by(id = id)
        if get_result > 0:
            session['name'] = get_result['name']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                #             (txt_body, id, uid))
                # # Commit cursor
                # mysql.connection.commit()
                msg = Messages(body=txt_body,msg_by=id,msg_to=uid)
                db.session.add(msg)
                db.session.commit()

            # Get users
            # cur.execute("SELECT * FROM users")
            # users = cur.fetchall()
            users = Users.query.all()

            # Close Connection
            # cur.close()
            return render_template('chat_room.html', users=users, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        # Create cursor
        # cur = mysql.connection.cursor()
        # # Get message
        # cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
        #             "ORDER BY id ASC", (id, uid, uid, id))
        # chats = cur.fetchall()
        # # Close Connection
        # cur.close()
        chats = Messages.query.filter(msg_by = id, msg_to = uid).filter(msg_by = uid, msg_to = id)

        return render_template('chats.html', chats=chats, )
    return redirect(url_for('login'))





@app.route('/magazines', methods=['GET', 'POST'])
def magazines():
    form = OrderForm(request.form)
    # Create cursor
    # cur = mysql.connection.cursor()
    # Get message
    values = 'magazines'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    # products = cur.fetchall()
    # Close Connection
    page = request.args.get("page",1,type=int)
    products = Products.query.filter_by(category = values).order_by(Products.date.desc()).paginate(page=page,per_page=20)
    # cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        email = form.email.data
        quantity = 1
        pid = request.args['order']
        session['pid']= pid
        # Create Cursor
        # curs = mysql.connection.cursor()
        phone = format_phone(mobile)

        if 'pid' in session:
            uid = session['pid']
            # curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
            #              "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            #              (uid, pid, name, mobile, order_place, quantity, now_time))
            order = Orders(uid=uid,ofname=name,quantity=quantity,mobile=mobile,email=email,odate=datetime.datetime.utcnow())
            id = uid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)
        else:
            order = Orders(uid=pid,ofname=name,mobile=mobile,email=email,quantity=quantity,odate=datetime.datetime.utcnow())
            id = pid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)
        #     curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
        #                  "VALUES(%s, %s, %s, %s, %s, %s)",
        #                  (pid, name, mobile, order_place, quantity, now_time))
        # # Commit cursor

        db.session.add(order)
        db.session.commit()
        # mysql.connection.commit()

        # Close Connection
        # cur.close()

        flash('Order successful', 'success')
        return render_template('magazines.html', magazines=products, form=form)
    if 'view' in request.args:
        product_id = (request.args['view'])
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        products = Products.query.filter_by(id = product_id).all()
        # print(type(product_id))
        # print(product)
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        print('Execution time: ' + str(execution_time) + ' usec')
        if 'uid' in session:
            uid = session['uid']
            # Create cursor
            # cur = mysql.connection.cursor()
            # cur.execute("SELECT * FROM product_view WHERE user_id=%s AND product_id=%s", (uid, product_id))
            # result = cur.fetchall()
            result = ProductView.query.filter_by(user_id= uid).filter(product_id = product_id)
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                # cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                #             (now_time, uid, product_id))
                ProductView.query.filter(user_id = uid).filter(product_id = product_id).update(dict(date = now_time))
            else:
                # cur.execute("INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)", (uid, product_id))
                # mysql.connection.commit()
                prod = ProductView(user_id=uid,product_id= product_id)
                db.session.add(prod)
            db.session.commit()
        return render_template('view_product.html', x=x, magazines=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        session['pid']= product_id

        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        #         # product = curso.fetchall()
        product = Products.query.filter_by(id = product_id).all()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, products=product, form=form, domain=pesa.domain)
    return render_template('magazines.html', magazines=products, form=form)


@app.route('/comics', methods=['GET', 'POST'])
def comics():
    form = OrderForm(request.form)
    # Create cursor
    # cur = mysql.connection.cursor()
    # Get message
    values = 'comics'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    # products = cur.fetchall()
    # # Close Connection
    # cur.close()
    page = request.args.get("page",1,type=int)
    products = Products.query.filter_by(category = values).order_by(Products.date.desc()).paginate(page=page,per_page=20)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        email = form.email.data
        quantity = 1
        pid = request.args['order']
        phone = format_phone(mobile)
        session['pid']= pid
        order = Orders(uid=pid, ofname=name, quantity=quantity, mobile=phone, email=email,
                       odate=datetime.datetime.utcnow())
        db.session.add(order)
        db.session.commit()
        prod = Products.query.filter_by(id=pid).first()
        # pesa.transaction(prod.price, phone)
        mdoh = pesa.transaction(prod.price,phone)
        if mdoh:
            flash('Order successful', 'success')
            return redirect(url_for('link.html', product=prod))
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        # products = curso.fetchall()
        products = Products.query.filter_by(id = q).all()
        return render_template('view_product.html', x=x, magazines=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        session['pid']= product_id

        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        product = Products.query.filter_by(id = product_id).all()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, products=product, form=form,domain=pesa.domain)
    return render_template('comics.html', comics=products, form=form)


@app.route('/textbooks', methods=['GET', 'POST'])
def textbooks():
    form = OrderForm(request.form)
    # Create cursor
    # cur = mysql.connection.cursor()
    # Get message
    values = 'textbooks'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    # products = cur.fetchall()
    # # Close Connection
    # cur.close()
    page = request.args.get("page",1,type=int)
    products = Products.query.filter_by(category = values).order_by(Products.date.desc()).paginate(page=page,per_page=20)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        email = form.email.data
        quantity = 1
        pid = request.args['order']
        phone = format_phone(mobile)
        session['pid']= pid

        # Create Cursor
        # curs = mysql.connection.cursor()
        if 'pid' in session:
            uid = session['pid']
            # curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
            #              "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            #              (uid, pid, name, mobile, order_place, quantity, now_time))
            order = Orders(uid=uid,ofname=name,quantity=quantity,mobile=phone,email=email,odate=datetime.datetime.utcnow())
            id = uid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)
        else:
            order = Orders(uid=pid, ofname=name,mobile=phone, email=email,quantity= quantity,odate=datetime.datetime.utcnow())
            id = pid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)

            # curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
            #              "VALUES(%s, %s, %s, %s, %s, %s)",
            #              (pid, name, mobile, order_place, quantity, now_time))
        db.session.add(order)
        db.session.commit()

        # # Commit cursor
        # mysql.connection.commit()
        #
        # # Close Connection
        # cur.close()

        flash('Order successful', 'success')
        return render_template('textbooks.html', textbooks=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        # products = curso.fetchall()
        products = Products.query.filter_by(id= q)
        return render_template('view_product.html', x=x, magazines=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        session['pid']= product_id

        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        product = Products.query.filter_by(id = product_id).all()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, products=product, form=form,domain=pesa.domain)
    return render_template('textbooks.html', textbooks=products, form=form)


@app.route('/newspapers', methods=['GET', 'POST'])
def newspapers():
    form = OrderForm(request.form)
    # Create cursor
    # cur = mysql.connection.cursor()
    # Get message
    values = 'newspapers'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    # products = cur.fetchall()
    # # Close Connection
    # cur.close()
    page = request.args.get("page",1,type=int)
    products = Products.query.filter_by(category = values).order_by(Products.date.desc()).paginate(page=page,per_page=20)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        email = form.email.data
        quantity = 1
        pid = request.args['order']
        phone = format_phone(mobile)
        session['pid']= pid

        # Create Cursor
        # curs = mysql.connection.cursor()
        if 'pid' in session:
            uid = session['pid']
            # curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
            #              "VALUES(%s, %s, %s, %s, %s, %s, %s)",
            #              (uid, pid, name, mobile, order_place, quantity, now_time))
            order = Orders(uid=uid,ofname=name,quantity=quantity,mobile=phone,email=email,odate=datetime.datetime.utcnow())
            id = uid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)
        else:
            order = Orders(uid=pid, ofname=name,mobile=phone,email=email,quantity= quantity,odate=datetime.datetime.utcnow())
            id = pid
            prod = Products.query.filter_by(id=id).first()
            pesa.transaction(prod.price, phone)

        #     curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
        #                  "VALUES(%s, %s, %s, %s, %s, %s)",
        #                  (pid, name, mobile, order_place, quantity, now_time))
        # # Commit cursor
        # mysql.connection.commit()
        # # Close Connection
        # cur.close()
        db.session.add(order)
        db.session.commit()

        flash('Order successful', 'success')
        return render_template('newspapers.html', newspapers=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        # products = curso.fetchall()
        products = Products.query.filter_by(id = q).all()
        return render_template('view_product.html', x=x, magazines=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        session['pid']= product_id

        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        product = Products.query.filter_by(id = product_id).all()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, products=product, form=form, domain=pesa.domain)
    return render_template('newspapers.html', newspapers=products, form=form)


@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # GEt user form
        username = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        # cur = mysql.connection.cursor()

        # Get user by username
        # result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])
        result = Admin.query.filter_by(email = username)

        if result :
            # Get stored value
            # data = cur.fetchone()
            data = Admin.query.filter_by(email = username).first()
            password = data.password
            uid = data.id
            name = data.firstname
            print(password)

            # Compare password
            # if sha256_crypt.verify(password_candidate, password):
            if password_candidate == password:
                # passed
                session['admin_logged_in'] = True
                session['admin_uid'] = uid
                session['admin_name'] = name

                return redirect(url_for('admin'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Username not found', 'danger')
            # Close connection
            # cur.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    # curso = mysql.connection.cursor()
    # num_rows = curso.execute("SELECT * FROM products")
    num_rows = db.session.query(Products).count()
    #result = curso.fetchall()
    result = Products.query.all()
    # order_rows = curso.execute("SELECT * FROM orders")
    # users_rows = curso.execute("SELECT * FROM users")
    order_rows = db.session.query(Orders).count()
    users_rows = db.session.query(Users).count()
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    # curso = mysql.connection.cursor()
    # num_rows = curso.execute("SELECT * FROM products")
    # order_rows = curso.execute("SELECT * FROM orders")
    # result = curso.fetchall()
    # users_rows = curso.execute("SELECT * FROM users")
    num_rows = db.session.query(Products).count()
    order_rows = db.session.query(Orders).count()
    result = Orders.query.all()
    users_rows = db.session.query(Users).count()
    return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/users')
@is_admin_logged_in
def users():
    # curso = mysql.connection.cursor()
    # num_rows = curso.execute("SELECT * FROM products")
    # order_rows = curso.execute("SELECT * FROM orders")
    # users_rows = curso.execute("SELECT * FROM users")
    # result = curso.fetchall()
    num_rows = db.session.query(Products).count()
    order_rows =db.session.query(Orders).count()
    users_rows = db.session.query(Users).count()
    result = Users.query.all()

    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form['date']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        author = request.form['author']
        country = request.form['countryOrigin']
        edition = request.form['edition']
        link = request.form['link']
        file = request.files['picture']
        if name and price and description and author and country and edition and link and file:
            allowed = {"."}.union(string.ascii_letters)
            pic = file.filename
            photo =  "".join([letter for letter in pic if letter in allowed])
            picture = photo.replace(" ", "")
            print(file)
            print(picture)
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                bucket = s3.Bucket(BUCKET_NAME)
                bucket.Object('static/image/product/'+category+'/'+picture).put(Body=file, ACL='public-read')
                # fp = open(file, 'rb')
                # https: // s3.us - east - 2.amazonaws.com / wanderift / static / image / product / comics / Beano % E2 % 80 % 932February2019.jpg
                # s3.Bucket(BUCKET_NAME).upload_file(Filename = pic, Key=picture)
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # Create Cursor
                    # curs = mysql.connection.cursor()
                    # curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                    #              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                    #              (name, price, description, available, category, item, code, picture))
                    # mysql.connection.commit()
                    product = Products(p_name=name,price= price,description=description,author=author,countryOrigin=country,edition=edition,link=link,picture=picture,pubdate=date,category=category)
                    db.session.add(product)
                    db.session.commit()
                    # product_id = curs.lastrowid
                    product_id = product.id
                    # curs.execute("INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    prod_lvl = ProductLevel(product_id=product_id, v_shape='no', polo='no', design='yes', chain='yes', leather='yes', hook='no', color='no', formal='yes', converse='no',loafer='no',clean_String='yes')
                    db.session.add(prod_lvl)
                    db.session.commit()
                    if category == 'magazines':
                        level = request.form.getlist('magazines')
                        yes = 'yes'
                        for lev in level:
                            ProductLevel.query.filter_by(id=product_id).update({''.format(lev):yes})
                            db.session.commit()
                            # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            # curs.execute(query, (yes, product_id))
                            # # Commit cursor
                            # mysql.connection.commit()
                    elif category == 'comics':
                        level = request.form.getlist('comics')
                        for lev in level:
                            yes = 'yes'
                            ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            db.session.commit()
                            # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            # curs.execute(query, (yes, product_id))
                            # Commit cursor
                            # mysql.connection.commit()
                    elif category == 'textbooks':
                        level = request.form.getlist('textbooks')
                        for lev in level:
                            yes = 'yes'
                            ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            db.session.commit()
                            # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            # curs.execute(query, (yes, product_id))
                            # Commit cursor
                            # mysql.connection.commit()
                    elif category == 'newspapers':
                        level = request.form.getlist('newspapers')
                        for lev in level:
                            yes = 'yes'
                            ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            db.session.commit()
                            # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            # curs.execute(query, (yes, product_id))
                            # Commit cursor
                            # mysql.connection.commit()
                    else:
                        flash('Product level not found', 'danger')
                        return redirect(url_for('admin_add_product'))
                    # Close Connection
                    # curs.close()

                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        # curso = mysql.connection.cursor()
        # res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        # product = curso.fetchall()
        product =Products.query.filter_by(id= product_id).all()
        # curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        # product_level = curso.fetchall()
        product_level = ProductLevel.query.filter_by(id= product_id)
        if product:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                author = request.form['author']
                category = request.form['category']
                countryOrigin = request.form['countryOrigin']
                edition = request.form['edition']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and author and category and countryOrigin and edition and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            # cur = mysql.connection.cursor()
                            # exe = curso.execute(
                            #     "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                            #     (name, price, description, available, category, item, code, pic, product_id))
                            # print(exe)
                            Products.query.filter_by(id= product_id).update(dict(pName=name,price=price,description=description,author=author,category=category,countryOrigin=countryOrigin,edition=edition,picture=pic))
                            # if exe:
                            #     if category == 'magazines':
                            #         level = request.form.getlist('magazines')
                            #         for lev in level:
                            #             yes = 'yes'
                            #             ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            #             db.session.commit()
                            #             # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                            #             #     field=lev)
                            #             # cur.execute(query, (yes, product_id))
                            #             # Commit cursor
                            #             # mysql.connection.commit()
                            #     elif category == 'comics':
                            #         level = request.form.getlist('comics')
                            #         for lev in level:
                            #             yes = 'yes'
                            #             ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            #             db.session.commit()
                            #             # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                            #             #     field=lev)
                            #             # cur.execute(query, (yes, product_id))
                            #             # Commit cursor
                            #             # mysql.connection.commit()
                            #     elif category == 'textbooks':
                            #         level = request.form.getlist('textbooks')
                            #         for lev in level:
                            #             yes = 'yes'
                            #             ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            #             db.session.commit()
                            #             # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                            #             #     field=lev)
                            #             # cur.execute(query, (yes, product_id))
                            #             # Commit cursor
                            #             # mysql.connection.commit()
                            #     elif category == 'newspapers':
                            #         level = request.form.getlist('newspapers')
                            #         for lev in level:
                            #             yes = 'yes'
                            #             ProductLevel.query.filter_by(id=product_id).update({''.format(lev): yes})
                            #             db.session.commit()
                            #             # query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                            #             #     field=lev)
                            #             # cur.execute(query, (yes, product_id))
                            #             # Commit cursor
                            #             # mysql.connection.commit()
                            #     else:
                            #         flash('Product level not fund', 'danger')
                            #         return redirect(url_for('admin_add_product'))
                            #     flash('Product updated', 'success')
                            #     return redirect(url_for('edit_product'))

                            flash('Data updated', 'success')
                            return redirect(url_for('edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('edit_product.html', product=product,
                                           product_level=product_level)
            else:
                print('get')
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'q' in request.args:
        q = request.args['q']
        # # Create cursor
        # cur = mysql.connection.cursor()
        # # Get message
        # query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        # cur.execute(query_string, ('%' + q + '%',))
        # products = cur.fetchall()
        # # Close Connection
        # cur.close()
        # products = Products.query.filter(or_(Products.pName.like(q),Products.pubdate.like(q))).all()
        page = request.args.get("page", 1, type=int)
        products = Products.query.whoosh_search(q).all()
            # .paginate(page=page,per_page=20)
        for product in products:
            print(products)
        flash('Showing result for: ' + q, 'success')
        return render_template('search.html', products=products)
    else:
        flash('Search again', 'danger')
        return render_template('search.html')


@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        # result = curso.fetchone()
        result = Users.query.filter_by(id=q).first()
        if result:
            if result.id == session['uid']:
                # curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                # res = curso.fetchall()
                res = Orders.query.filter_by(uid = session['uid']).order_by(Orders.id.asc())
                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        # curso = mysql.connection.cursor()
        # curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        # result = curso.fetchone()
        result = Users.query.filter_by(id= q).first()
        if result:
            if result.id == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data
                    # # Create Cursor
                    # cur = mysql.connection.cursor()
                    # exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                    #                   (name, email, password, mobile, q))
                    exe = Users.query.filter_by(id=q).update(dict(name=name,email=email,password=password,mobile=mobile))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/developer', methods=['POST', 'GET'])
def developer():
    # id = session['pid']
    # print(id)
    prod = Products.query.filter_by(id=1).first()
    print(prod.link)
    # form = DeveloperForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     q = form.id.data
    #     # curso = mysql.connection.cursor()
    #     # result = curso.execute("SELECT * FROM products WHERE id=%s", (q,))
    #     result = Products.query.filter_by(id= q)
    #     if result > 0:
    #         x = content_based_filtering(q)
    #         wrappered = wrappers(content_based_filtering, q)
    #         execution_time = timeit.timeit(wrappered, number=0)
    #         seconds = ((execution_time / 1000) % 60)
    #         return render_template('developer.html', form=form, x=x, execution_time=seconds)
    #     else:
    #         nothing = 'Nothing found'
    #         return render_template('developer.html', form=form, nothing=nothing)
    # else:
    return render_template('link.html', product=prod)


@app.route('/requests', methods=['GET', 'POST'])
def myrequests():
    form = RequestForm(request.form)
    if request.method == 'POST' and form.validate():
        category = form.category.data
        title = form.title.data
        publication_month = form.pubmonth.data
        description = form.description.data

        record = Request(category, title,publication_month, description, status="pending")
        db.session.add(record)
        db.session.commit()
        flash('Request Received', 'success')
        return redirect(url_for('index'))
    return render_template('modal_order.html', form=form)


@app.route('/fileserve')
def servefile():
    id = session['pid']
    print(id)
    prod = Products.query.filter_by(id=id).first()
    print(prod.link)
    return render_template("link.html", product=prod) # file not opening


@app.route('/callback', methods= ['POST'])
def callback():
    if request.method == 'POST':
        resp = request.json
        print(resp)
        print(type(resp))
        str(resp)
        resp = json.dumps(resp)
        print(type(resp))
        data = json.loads(resp)

        if data['Body']['stkCallback']['ResultCode'] == "0":
            if 'pid' in session:
                prod = Products.query.filter_by(id=session['pid']).first()
                return redirect(url_for('servefile', product=prod))
            else:
                prod = Products.query.filter_by(id=request.args['order']).first()
                return redirect(url_for('servefile', product=prod))
        return redirect(url_for(str('index')))


@app.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://"+pesa.domain+"/execute",
            "cancel_url": "http://"+pesa.domain+"/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "1.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "1.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})



@app.route('/execute', methods=['POST'])
def execute():
    id = session['pid']
    print(id)
    prod = Products.query.filter_by(id=id).first()
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    r = requests.get(prod.link)
    # filename= prod.picture.replace(".", "")
    # with open(filename+".pdf", 'wb') as f:
    #     f.write(r.content)
    print('Execute success!')
    # return redirect('https://www.google.com/', code=302)
    # return redirect(str(prod.link), code=302)
    # return render_template("link.html", product=prod)
    return render_template("link.html", product=prod)