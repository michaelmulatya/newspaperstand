from core import db, app
import flask_whooshalchemy as wa
from datetime import datetime
from whoosh.analysis import StemmingAnalyzer

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(125))
    lastname = db.Column(db.String(125))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(25))
    address = db.Column(db.String)
    password = db.Column(db.String(100))
    type = db.Column(db.String(20))
    confirmcode = db.Column(db.String(10))

    def __init__(self, firstname, lastname, email, mobile, address,
                 password, type, confirmcode):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.mobile = mobile
        self.address = address
        self.password = password
        self.type = type
        self.confirmcode = confirmcode


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    ofname = db.Column(db.String)
    quantity = db.Column(db.Integer)
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))
    odate = db.Column(db.String, nullable=False, default=datetime.now)

    def __init__(self, uid, ofname, quantity, mobile, email, odate):
        self.uid = uid
        self.ofname = ofname
        self.quantity = quantity
        self.mobile = mobile
        self.email = email
        self.odate = odate


class Products(db.Model):
    __searchable__ = ['pName','pubdate','description']
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    pName = db.Column(db.String(100))
    pubdate = db.Column(db.String(10))
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    category = db.Column(db.String(100))
    countryOrigin = db.Column(db.String(100))
    author = db.Column(db.String(100))
    picture = db.Column(db.String)
    edition = db.Column(db.String(50))
    link = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, p_name,pubdate, price, description, countryOrigin, category, author, edition, picture,link):
        self.pName = p_name
        self.pubdate = pubdate
        self.price = price
        self.description = description
        self.countryOrigin = countryOrigin
        self.category = category
        self.author = author
        self.edition = edition
        self.picture = picture
        self.link = link


class ProductLevel(db.Model):
    __tablename__ = 'product_level'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    v_shape = db.Column(db.String(10))
    polo = db.Column(db.String(10))
    clean_String = db.Column(db.String(10))
    design = db.Column(db.String(10))
    chain = db.Column(db.String(10))
    leather = db.Column(db.String(10))
    hook = db.Column(db.String(10))
    color = db.Column(db.String(10))
    formal = db.Column(db.String(10))
    converse = db.Column(db.String(10))
    loafer = db.Column(db.String(10))

    def __init__(self, product_id, v_shape, polo, clean_String, design, chain, leather, hook, color, formal, converse,
                 loafer):
        self.product_id = product_id
        self.v_shape = v_shape
        self.polo = polo
        self.clean_String = clean_String
        self.design = design
        self.chain = chain
        self.leather = leather
        self.hook = hook
        self.color = color
        self.formal = formal
        self.converse = converse
        self.loafer = loafer


class ProductView(db.Model):
    __tablename__ = 'product_view'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    date = db.Column(db.String, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, product_id, date):
        self.user_id = user_id
        self.product_id = product_id
        self.date = date


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    username = db.Column(db.String(25))
    password = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    reg_time = db.Column(db.String, default=datetime.utcnow)
    online = db.Column(db.String(1), default=0)
    activation = db.Column(db.String(3))

    def __init__(self, name, email, username, password, mobile, reg_time, online, activation):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.mobile = mobile
        self.reg_time = reg_time
        self.online = online
        self.activation = activation


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String)
    msg_by = db.Column(db.Integer)
    msg_to = db.Column(db.Integer)

    def __init__(self, body, msg_by, msg_to):
        self.body = body
        self.msg_by = msg_by
        self.msg_to = msg_to

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(20))
    title = db.Column(db.String(50))
    pubmonth = db.Column(db.String(20))
    description = db.Column(db.String)
    status = db.Column(db.String(15))

    def __init__(self, category, title, pubmonth, description, status):
        self.category = category
        self.title = title
        self.pubmonth = pubmonth
        self.description = description
        self.status = status

wa.whoosh_index(app, Products)