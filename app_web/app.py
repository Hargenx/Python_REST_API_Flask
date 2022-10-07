# pip install flask
# pip install flask_sqlalchemy
# pip install flask_marshmallow
# pip install marshmallow-sqlalchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

diretorio = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretorio, 'app_clube.sqlite')
db = SQLAlchemy(app)
mm = Marshmallow(app)

class Clube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(144), unique=False)
    clube = db.Column(db.String(100), unique=False)


    def __init__(self, nome, clube):
        self.nome = nome
        self.clube = clube


class ClubeEsquema(mm.Schema):
    class Meta:
        fields = ('nome', 'clube')


clube_scheme = ClubeEsquema()
clubes_scheme = ClubeEsquema(many=True)

# Endpoint criar novo clube
@app.route('/clube', methods=["POST"])
def add_clube():
    nome = request.json['nome']
    clube = request.json['clube']

    novo_clube = Clube(nome, clube)
    db.session.add(novo_clube)
    db.session.commit()

    clube = Clube.query.get(novo_clube.id)

    return clube_scheme.jsonify(clube)


# Endpoint para todos clubes
@app.route("/clubes", methods=["GET"])
def get_clubes():
    todos_clubes = Clube.query.all()
    resultado = clubes_scheme.dump(todos_clubes)
    return jsonify(resultado)


# Endpoint para somente um clube
@app.route("/clube/<id>", methods=["GET"])
def get_clube(id):
    clube = Clube.query.get(id)
    return clube_scheme.jsonify(clube)


# Endpoint atualizar clube
@app.route("/clube/<id>", methods=["PUT"])
def clube_update(id):
    clube = Clube.query.get(id)
    nome = request.json['nome']
    time = request.json['clube']

    clube.nome = nome
    clube.time = time

    db.session.commit()
    return clube_scheme.jsonify(clube)


# Endpoint apagar um registro
@app.route("/clube/<id>", methods=["DELETE"])
def clube_delete(id):
    clube = Clube.query.get(id)
    db.session.delete(clube)
    db.session.commit()

    return "clube apagado com sucesso"


if __name__ == '__main__':
    app.run(debug=True)