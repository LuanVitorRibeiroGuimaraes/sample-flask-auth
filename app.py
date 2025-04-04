from flask import Flask, request, jsonify
from models.User import User
from login import login_manager
from flask_login import login_user, current_user, logout_user, login_required
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key' #chave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' #URL de conexão

db.init_app(app)
login_manager.init_app(app)


login_manager.login_view = 'login' 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        #Login
        user = User.query.filter_by(username = username).first()
        
        if user and user.password == password:
            login_user(user)
            return jsonify({'message':'Successfully auth'})
        
    return jsonify({'message':'Invalid Credential'}), 400

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message':'Logout successfully'})

@app.route('/user', methods = ['POST'])
@login_required
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = User(username = username, password = password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'User registred succesfully!'})
    
    return jsonify({'message':'Invalid credentials'}), 400

@app.route('/hello-world', methods = ['GET'])
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug = True)
