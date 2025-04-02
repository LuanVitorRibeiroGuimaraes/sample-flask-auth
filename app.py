from flask import Flask, request, jsonify
from models.User import User
from login import login_manager
from flask_login import login_user, current_user
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key' #chave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' #URL de conexão

#session <- armazena a conexão ativa, possui tempo limite
db.init_app(app)
login_manager.init_app(app) #Vincula o Flask-Login ao app.

#view de login
login_manager.login_view = 'login' #Define a página para onde usuários não logados serão redirecionados.


# Antes de acessar uma rota protegida (@login_required)
# Se um usuário tentar acessar uma rota protegida, o Flask precisa verificar:
# O usuário está autenticado?
# Ele tem permissão para acessar essa página?
# Para isso, recupera o usuário usando o user_loader.Antes de acessar uma rota protegida (@login_required)
# Se um usuário tentar acessar uma rota protegida, o Flask precisa verificar:
# O usuário está autenticado?
# Ele tem permissão para acessar essa página?
# Para isso, recupera o usuário usando o user_loader.

@login_manager.user_loader #Diz ao Flask-Login como carregar o usuário a partir do ID salvo na sessão.
def load_user(user_id): #Busca e retorna o usuário correspondente ao ID. verifica permissões, acessa atributos e verifica se está autenticado
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
            login_user(user) #loga o usuário (salva o id na sessão)
            # print(current_user.is_authenticated)
            return jsonify({'message':'Successfully auth'})
        
    return jsonify({'message':'Invalid Credential'}), 400


@app.route('/hello-world', methods = ['GET'])
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug = True)
