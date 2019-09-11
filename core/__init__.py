from flask import Flask
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_cdn import CDN
# import paypalrestsdk
# import flask_whooshalchemy



app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'core/static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# app.config['CDN_DOMAIN'] = 's3.us-east-2.amazonaws.com'
# CDN(app)

basedir = os.path.abspath(os.path.dirname(__file__))
# STATIC_ROOT = os.path.join(basedir, 'staticfiles')
# STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(basedir, 'static'),
# )
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
POSTGRES = {
    'user': 'crhwmuskdlrkvy',
    'pw': '58eac07f790dab6e1507d163bae6103770bccb341e83ad4c0055bb00869e90a0',
    'db': 'dfflrmrkmt6u1s',
    'host': 'ec2-54-221-253-228.compute-1.amazonaws.com',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['WHOOSH_BASE'] = 'whoosh'
db = SQLAlchemy(app)
Migrate(app,db)



from views import core

app.register_blueprint(core)

# Config MySQL
# mysql = MySQL()
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'core'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#
# # Initialize the app for use with this MySQL class
# mysql.init_app(app)
