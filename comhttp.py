from flask import Flask, render_template, request, flash, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = "palavra-secreta123"

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://magnusfelinto:magnusmv123@cluster0.fphqfh4.mongodb.net/") 
db = client["test"]
collection = db.get_collection("prefeitos")

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
        # Se encontrou o documento, redireciona para outra página
        return redirect("http://127.0.0.1:8050/")  # Substitua pelo URL desejado
    else:
        # Se não encontrou, exibe mensagem de erro e redireciona para a página de login
        flash("Credenciais inválidas. Tente novamente.")
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)