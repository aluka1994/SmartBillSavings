

import os


class Config: #production
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    cloud_storage_bucket = os.environ['CLOUD_STORAGE_BUCKET']
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@/'+db_name+'?unix_socket=/cloudsql/'+cloud_sql_connection_name+"?charset=utf8mb4"
'''


class Config: #development
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = "ccnew-275119.appspot.com"
    db_user = "root"
    db_pass = "raja1234"
    db_name = "bdb"
    cloud_storage_bucket = "ccnew-275119:us-east1:clouddb"
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@localhost/'+db_name+"?charset=utf8mb4"
'''