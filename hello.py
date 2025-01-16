from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de dados para Alunos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplina = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    data_hora_brasilia = datetime.now(brasilia_tz).strftime('%d/%m/%Y %H:%M')
    dados = {
        'nome': 'Luis de Moura Neto',
        'prontuario': 'PT3019861',
        'data_hora': data_hora_brasilia,
    }
    return render_template('index.html', dados=dados)

@app.route('/cadastro_alunos', methods=['GET', 'POST'])
def cadastro_alunos():
    if request.method == 'POST':
        nome_aluno = request.form['nome']
        disciplina_aluno = request.form['disciplina']
        novo_aluno = Aluno(nome=nome_aluno, disciplina=disciplina_aluno)
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('cadastro_alunos'))
    
    alunos = Aluno.query.all()
    return render_template('cadastro_alunos.html', alunos=alunos)

@app.route('/cadastro_professores')
@app.route('/cadastro_disciplinas')
def nao_disponivel():
    return render_template('nao_disponivel.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
