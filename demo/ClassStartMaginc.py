from typing import Any
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Stu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    _password_hash = db.Column(db.String(128))

    def get_password(self):
        return self._password_hash
    
    def set_password(self, value):
        self._password_hash = value

    def del_password(self):
        del self._password_hash

    password = property(get_password, set_password)

data = {
    "id": 1,
    "username": "farmer",
    "password": "farmer233"
}
try:
    stu = Stu(**data)
    print(stu.password)
except Exception as e :
    print(e)