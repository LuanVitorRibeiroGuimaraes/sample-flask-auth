from database import db
from flask_login import UserMixin

#db.Model gera um construtor automático
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique_key = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)