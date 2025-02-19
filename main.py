import os
import functions_framework

from flask import Flask, request, redirect, render_template, session
from urllib.parse import urlencode
from flask_session import Session

app = Flask(__name__)

# Configuração da sessão para armazená-la no servidor
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SECRET_KEY'] = os.urandom(24)

# Inicializa a sessão corretamente
Session(app)

@app.route('/<id_campanha>', methods=['GET'])
def login(id_campanha):
    session['id_campanha'] = id_campanha        
    return render_template("forms.html")


@app.route('/authorize', methods=['POST'])
def authorize():
    name = request.form.get("name")
    email = request.form.get("email")
    id_campanha = session.get('id_campanha')

    print(email)
    print(name)

    base_url = f"https://tracksale.co/dl/{id_campanha}"
    params = {'name': name, 'email': email}
    new_url = f"{base_url}?{urlencode(params)}"

    print(new_url)

    return redirect(new_url)


@functions_framework.http
def main(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()


if __name__ == '__main__':
    app.run(debug=True)
