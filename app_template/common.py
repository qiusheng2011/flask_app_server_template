
import functools

import pymysql

from flask import current_app as app , g

dbconnect = None

def get_db():
    if "db_connect" not in g:
        prefix_ = app.config["flask_app_template"]+"_"
        dbconnect = pymysql.connect(
            host=app.config[prfix_+"mysql_host"],
            port=app.cofig[prfix_+"mysql_port"],
            user=app.config[prfix_+"mysql_user"],
            password=app.config[prfix_+'mysql_password'],
            database=app.config[prfix_+'mysql_database']
        )
        g["db_connect"]=dbconnect
        return dbconnect
    else:
        return g["dbconnect"]

def close_db(e=None):
    db = g.pop("db_connect",None)
    if db is not None:
        db.close()

def init_db_app(app):
    app.teardown_appcontext(close_db)