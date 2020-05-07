# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_pubsub_setup]
import base64
from google.cloud import pubsub_v1
import json
import os
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from app.googleOCR import _get_ocr_tokens
from datetime import datetime
from flask_login import UserMixin
from flask_script import Manager

cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@/'+db_name+'?unix_socket=/cloudsql/'+cloud_sql_connection_name+"?charset=utf8mb4"
# Set these in the environment variables for the function
# This must be set, determine which is best for you
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

# [START functions_pubsub_subscribe]
#command
#gcloud functions deploy Translate --runtime=python37 --entry-point=subscribe --trigger-topic=ocr --set-env-vars GOOGLE_CLOUD_PROJECT=ccnew-275119
# Triggered from a message on a Cloud Pub/Sub topic.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    userimages = db.relationship('userImage', backref='timage', lazy=True)
    productname = db.relationship('Product', backref='productname', lazy=True)
    grocerylistname = db.relationship('GroceryList', backref='grocerylist', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class userImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(100), nullable=False)
    imageUrl = db.Column(db.String(1000),nullable=False)
    imageDate = db.Column(db.DateTime,default=datetime.utcnow)
    notify = db.Column(db.Boolean,default=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
       return {c.name: str(getattr(self, c.name)).rstrip("\n") for c in self.__table__.columns}

    def __repr__(self):
        return 'userImage %r %r %r>' % (self.imageName, self.imageUrl, self.notify)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    price =  db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Float,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}','{self.purchase_date}','{self.quantity}')"


class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(300), nullable=False)
    quantity = db.Column(db.Float,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"GroceryList('{self.id}', '{self.productName}','{self.user_id}','{self.quantity}')"

def parseList(data,date,user):
    plist1 = []
    plist2 = []
    key1 = data[0].split(" ",1)
    key2 = data[1].split(" ",1)
    purchase_date = date
    for value in data[2:]:
        item = {}
        value=value.split(" ", 1)
        if len(value)==2:
            print(value)
            item[key1[0]] = value[0]
            item[key1[1]]= value[1]
            plist1.append(item)
        elif len(value)==1:
            print(value)
            if '$' in value[0]:
                item[key2[0]] = value[0].split('$')[1]
            else:
                item[key2[0]] = 0
            plist2.append(item)
    
    plist = []
    for i in range(0,len(plist2)):
        item = {}
        item['Product'] = plist1[i]['Product']
        item['Qty'] = plist1[i]['Qty']
        item['Total'] = plist2[i]['Total']
        item['Date'] = str(purchase_date)
        print(item)
        plist.append(item)
        if item['Total'] == "":
            item['Total'] = 0
        prod = Product(name=item['Product'],price=(item['Total']),quantity=float(item['Qty']),productname=user)
        db.session.add(prod)
        db.session.commit()
        print("sucessfully commited to db")
    return json.dumps(plist)

def getData(duser,tid):
    user = User.query.filter_by(username=duser.username).first_or_404()
    uimages = userImage.query.filter_by(id=tid).order_by(userImage.imageDate.desc())
    print(uimages)
    data = []
    for value in uimages:
        print(value.serialize())
        tempVal = value.serialize()
        if 'Lotus Market Mesa' in tempVal['content']:
            val = tempVal['content']
            val = val.split("\n")
            count = 0
            start=0
            end=0
            date = 0
            for tval in val:
                if 'Qty Product' in tval:
                    start = count
                elif 'Date:' in tval:
                    date = count
                elif 'Total:' in tval:
                    end=count
                    break
                count=count+1
            purch = val[date+1]
            val = val[start:end]
            val = parseList(val,purch,user)
            data.append(val)
    return str(data)
def subscribe(event, context):
    # Print out the data from Pub/Sub, to prove that it worked
    message = base64.b64decode(event['data'])
    pdata = json.loads(message)

    imPath = pdata['imPath']
    uid = pdata['uid']
    filename = pdata['filename']
    tid = pdata['tid']
    print(imPath)
    print(uid)
    print(filename)
    print(tid)
    user = User.query.filter_by(id=uid).first_or_404()
    content = _get_ocr_tokens(imPath)
    updateImage = userImage.query.filter_by(id=tid).first_or_404()
    updateImage.content = content
    db.session.commit()
    getData(user,int(tid))
# [END functions_pubsub_subscribe]