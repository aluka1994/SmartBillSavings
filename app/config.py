

import os



class ConfigProd:
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    cloud_storage_bucket = os.environ['CLOUD_STORAGE_BUCKET']
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@/'+db_name+'?unix_socket=/cloudsql/'+cloud_sql_connection_name
'''

class ConfigDev:
    SECRET_KEY = "somesecretkey"
    cloud_sql_connection_name = "ccnew-275119.appspot.com"
    db_user = "raja"
    db_pass = "cloudcc"
    db_name = "bdb"
    cloud_storage_bucket = "ccnew-275119:us-east1:clouddb"
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+db_user+':'+\
    db_pass+'@104.196.153.244:3306/'+db_name
'''    
   

    # db = sqlalchemy.create_engine(
    #     # Equivalent URL:
    #     # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    #     sqlalchemy.engine.url.URL(
    #         drivername="mysql+pymysql",
    #         username=db_user,
    #         password=db_pass,
    #         database=db_name,
    #         query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    #     ),
    #     # ... Specify additional properties here.
    #     # [START_EXCLUDE]
    #     # [START cloud_sql_mysql_sqlalchemy_limit]
    #     # Pool size is the maximum number of permanent connections to keep.
    #     pool_size=5,
    #     # Temporarily exceeds the set pool_size if no connections are available.
    #     max_overflow=2,
    #     # The total number of concurrent connections for your application will be
    #     # a total of pool_size and max_overflow.
    #     # [END cloud_sql_mysql_sqlalchemy_limit]
    #     # [START cloud_sql_mysql_sqlalchemy_backoff]
    #     # SQLAlchemy automatically uses delays between failed connection attempts,
    #     # but provides no arguments for configuration.
    #     # [END cloud_sql_mysql_sqlalchemy_backoff]
    #     # [START cloud_sql_mysql_sqlalchemy_timeout]
    #     # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    #     # new connection from the pool. After the specified amount of time, an
    #     # exception will be thrown.
    #     pool_timeout=30,  # 30 seconds
    #     # [END cloud_sql_mysql_sqlalchemy_timeout]
    #     # [START cloud_sql_mysql_sqlalchemy_lifetime]
    #     # 'pool_recycle' is the maximum number of seconds a connection can persist.
    #     # Connections that live longer than the specified amount of time will be
    #     # reestablished
    #     pool_recycle=1800,  # 30 minutes
    #     # [END cloud_sql_mysql_sqlalchemy_lifetime]
    #     # [END_EXCLUDE]
    # )
