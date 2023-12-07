
import functools

import pymysql

from flask import current_app as app , g


def get_db():
    if "db_connect" not in g:
        prefix_ = app.config["config_prefix"]+"_"
        g.dbconnect = pymysql.connect(
            host=app.config["mysql_host"],
            port=int(app.config["mysql_port"]),
            user=app.config["mysql_user"],
            password=app.config['mysql_password'],
            database=app.config['mysql_database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
      
        return g.dbconnect
    else:
        return g.dbconnect

def close_db(e=None):
    db = g.pop("db_connect",None)
    if db is not None:
        db.close()

def init_db_app(app):
    app.teardown_appcontext(close_db)