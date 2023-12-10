import functools
import re
from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    current_app as app
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from ..error import InvalidAPIUsage
from ..common import get_db


auth_path = Blueprint("auth", __name__, url_prefix="/auth")


class ResgisterUser(object):

    def __init__(self):
        self._email = None
        self._password = None
        self._first_name = None
        self._last_name = None
        self._nickname =None 

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value:str):
        if value:
            if re.match(r"[a-z0-9]+@[a-z]+.[a-z]+",value):
                self._email = value
            else:
                self._email = ""
        else:
            self._email = ""

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value:str):
        if value:
            self._password = generate_password_hash(value)
        else:
            self._password = None
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if re.match(r"[a-z0-9A-Z]+",value or ""):
            self._first_name = value
    
    @property
    def last_name(self):
        return self._last_name
    @last_name.setter
    def last_name(self,value):
        if re.match(r"[a-z0-9A-Z]+", value or ""):
            self._last_name = value
    
    @property
    def nickname(self):
        return self._nickname
    @nickname.setter
    def nickname(self, value):
        if re.match(r"[0-9a-zA-Z]+", value or ""):
            self._nickname = value

    def vaild(self):
        if self.last_name and self.first_name and self.nickname and self.email and self.password:
            return True
        else:
            return False


@auth_path.route("/register", methods=["POST"])
def resgister():
    if request.method != "POST":
        pass # TODO RASIE ERROR
    request_id = request.headers.get("requestid", None)

    register_user = ResgisterUser()
    register_user.email = request.form.get("email", None)
    register_user.password = request.form.get("password", None)
    register_user.first_name = request.form.get("first_name", "")
    register_user.last_name = request.form.get("last_name", "")
    register_user.nickname = request.form.get("nickname", None)

    if not register_user.vaild():
        raise InvalidAPIUsage("参数错误",payload={"request_id":request_id})
    
    with get_db().cursor() as cursor:
        select_user = "select id from account where email=%(email)s"
        cursor.execute(select_user,{"email":register_user.email})
        rst = cursor.fetchall()
        if rst:
            app.logger.info(f"{register_user.email} 注册失败", extra={"request_id":request_id})

            raise InvalidAPIUsage("用户已经存在",payload={"request_id":request_id})
        insert_user = "insert into account (email, password, first_name, last_name, nickname) value(%(email)s, %(password)s, %(first_name)s, %(last_name)s, %(nickname)s)"
        cursor.execute(insert_user,{
            "email":register_user.email,
            "last_name": register_user.last_name,
            "first_name": register_user.first_name,
            "password": register_user.password,
            "nickname":register_user.nickname
        })
        app.logger.info(f"{register_user.email} 注册成功")

        return {
            "status": 0,
            "message":"ok"
        }
    





