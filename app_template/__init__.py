#! -*- coding:utf8 -*-

from flask import Flask
from dotenv import load_dotenv

from .common import init_db_app

class AppFactory():

    @staticmethod 
    def create_app(env_file_prefix=""):
        app = Flask(__name__)
        if app.config['DEBUG']:
            load_dotenv("../env/dev.env")
        else:
            load_dotenv("../env/prod.env")
        app.config.from_prefixed_env("flask_app_template")
        app.config['config_prefix'] = "flask_app_template"
        
        # 初始化 db
        init_db_app(app)
        ## 引入视图

        return app

app = AppFactory.create_app()