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
    jsonify
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from ..error import InvalidAPIUsage


auth_path = Blueprint("auth", __name__, url_prefix="/auth")


class ResgisterUser(object):

    def __init__(self):
        self._email = None
        self._password = None
        self._first_name = None
        self._last_name = None
        self._nick_name =None 

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
    def nick_name(self):
        return self._nick_name
    @nick_name.setter
    def nick_name(self, value):
        if re.match(r"[0-9a-zA-Z]+", value or ""):
            self._nick_name = value

    def vaild(self):
        if self.last_name and self.first_name and self.nick_name and self.email and self.password:
            return True
        else:
            return False


@auth_path.route("/register", methods=["POST"])
def resgister():
    if request.method != "POST":
        pass # TODO RASIE ERROR

    resgister_user = ResgisterUser()
    resgister_user.email = request.form.get("email", None)
    resgister_user.password = request.form.get("password", None)
    resgister_user.first_name = request.form.get("first_name", "")
    resgister_user.last_name = request.form.get("last_name", "")
    resgister_user.nick_name = request.form.get("nick_name", None)

    if not resgister_user.vaild():
        raise InvalidAPIUsage("参数错误")
    
    





