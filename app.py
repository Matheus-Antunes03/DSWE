from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange, Length

app = Flask(__name__, template_folder='C:\\Users\\matheus_antunes2\\Documents\\DSWE\\web_forms_wtf\\templates')

app.config['SECRET_KEY'] = 'chave_secreta'

class ContatoForm(FlaskForm):
    nome = StringField(
        'Nome',
        validators=[
            DataRequired(message="O campo nome é obrigatório."),
            Length(min=2, max=50, message="O nome deve ter entre 2 e 50 caracteres.")
            ]
    )
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message="O campo email é obrigatório."),
            Email(message="Digite um endereço de e-mail válido.")
            ]
    )
    idade = IntegerField(
        'Idade',
        validators=[
            DataRequired(message="O campo idade é obrigatório."),
            NumberRange(min=0, max=120, message="A idade deve estar entre 0 e 120 anos")
            ]
    )
    mensagem = TextAreaField(
        'Mensagem',
        validators=[
            DataRequired(message="O campo mensagem é obrigatório.")
            ]
    )
    enviar = SubmitField(
        'Enviar'
    )
    
@app.route('/', methods=['GET', 'POST'])
def index():
    formulario = ContatoForm()
    if formulario.validate_on_submit():
        contato = {
            'nome': formulario.nome.data,
            'email': formulario.email.data,
            'idade': formulario.idade.data,
            'mensagem': formulario.mensagem.data
        }
        
        session['contato'] = contato
        
        return redirect(url_for('obrigado'))
    
    return render_template('formulario.html', formulario=formulario)

@app.route('/obrigado')
def obrigado():
    contato = session.get('contato', None)
    if contato is None:
        return redirect(url_for('index'))
    
    session.clear()
    
    return render_template('obrigado.html', contato=contato)
if __name__ == '__main__':
    app.run(debug=True)