from flask import Flask, render_template, request, flash, redirect, url_for, session
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = "palavra-secreta123"

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://magnusfelinto:magnusmv123@cluster0.fphqfh4.mongodb.net/")
db = client["test"]
collection = db.get_collection("prefeitos")

# Decorator para verificar autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index():
    usuario = request.form.get('email')
    senha = request.form.get('senha')
    
    # Verifica se o usuário e senha correspondem aos dados no MongoDB
    document = collection.find_one({"email": usuario, "senha": senha})
    
    if document:
        # Se encontrou o documento, define o usuário como autenticado na sessão
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        # Se não encontrou, exibe mensagem de erro e redireciona para a página de login
        flash("Credenciais inválidas. Tente novamente.")
        return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    from dashboard import init_dash
    init_dash(app)
    app.run(debug=True)