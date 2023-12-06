#! -*- coding:utf8 -*-



class AppFactory():

   @staticmethod 
    def create_app(self, config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)

        ## 初始化数据库

        ## 引入视图

        return app
