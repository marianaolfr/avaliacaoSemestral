import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_RECIPIENTS = os.getenv('MAILGUN_RECIPIENTS')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'a_difficult_and_secure_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
        'nome': 'Mariana Oliveira Ferreira',
        'prontuario': 'PT3019497',
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
