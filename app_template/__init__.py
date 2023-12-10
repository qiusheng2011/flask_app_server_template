#! -*- coding:utf8 -*-
import os
import logging
from flask import Flask,jsonify, request, json
from dotenv import load_dotenv

from .common import init_db_app
from .views.auth import auth_path
from .error import *
from .applogging import ApplicationLoggingSetting
json.provider.DefaultJSONProvider.ensure_ascii = False

current_path = os.path.realpath(os.path.dirname(__file__))

class AppFactory():

    @staticmethod 
    def create_app(env_file_prefix=""):
        app = Flask(__name__)
        app.config['DEBUG'] = bool(os.environ.get("FLASK_APP_TEMPLATE_DEBUG", False))
        if app.config['DEBUG']:
            load_dotenv(f"{current_path}/../env/{env_file_prefix}dev.env",interpolate=False)
        else:
            load_dotenv(f"{current_path}/../env/{env_file_prefix}prod.env", interpolate=False)
        app.config.from_prefixed_env("flask_app_template", loads=lambda x:x)
        app.config['config_prefix'] = "flask_app_template"

        # 日志配置
        logging_setting = ApplicationLoggingSetting("flask_app_template", app.config["logging_socket_host"], int(app.config["logging_socket_port"]))
        logging_setting.setting_logger()

        # 初始化 db
        init_db_app(app)
        ## 引入视图
        app.register_blueprint(auth_path)
        return app

app = AppFactory.create_app()

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

