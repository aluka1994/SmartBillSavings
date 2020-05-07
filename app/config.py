

import os


class Config: #production
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
    PUBSUB_VERIFICATION_TOKEN = os.environ['PUBSUB_VERIFICATION_TOKEN']
    CLOUD_URL = os.environ['CLOUD_URL']
    PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']
    PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@/'+db_name+'?unix_socket=/cloudsql/'+cloud_sql_connection_name+"?charset=utf8mb4"
'''


class Config: #development
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = "ccnew-275119.appspot.com"
    db_user = "raja"
    db_pass = "cloudcc"
    db_name = "bdb"
    CLOUD_STORAGE_BUCKET = "ccnew-275119.appspot.com"
    PUBSUB_VERIFICATION_TOKEN = "1234abc"
    PUBSUB_TOPIC = "cloud-builds"
    PROJECT = "ccnew-275119"
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@104.196.153.244:3306/'+db_name+"?charset=utf8mb4"

'''