from re import A
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Tabla Categoria
class Categoria(db.Model):
  cart_id = db.Column(db.Integer, primary_key=True)
  cat_nom = db.Column(db.String(100))
  cat_desp = db.Column(db.String(100))

  def __init__(self,cat_nom,cat_desp):
    self.cat_nom = cat_nom
    self.cat_desp = cat_desp


db.create_all()

#Esquema Categoria
class CategoriaSchema(ma.Schema):
  class Meta:
    fields = ('cat_id', 'cat_nom', 'cat_desp')

#Una sola respuesta
categoria_schema = CategoriaSchema()
#Cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET###################################
@app.route('/categoria', methods=['GET'])
def get_categorias():
  all_categorias = Categoria.query.all()
  result = categorias_schema.dump(all_categorias)
  return jsonify(result)


#GET x ID#######################################
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
  una_categoria = Categoria.query.get(id)
  return categoria_schema.jsonify(una_categoria)

#POST###########################################
@app.route('/categoria', methods=['POST'])
def insert_categoria():
  # data = request.get_json(force=True)
  cat_nom = request.json('cat_nom')
  cat_desp = request.json('cat_desp')

  nuevo_registro = Categoria(cat_nom, cat_desp)

  db.session.add(nuevo_registro)
  db.session.commit()
  return categoria_schema.jsonify(nuevo_registro)


#POST###########################################
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
  actualizarCategoria = Categoria.query.get(id)
  cat_nom = request.json['cat_nom']
  cat_desp = request.json['cat_desp']

  actualizarCategoria.cat_nom = cat_nom
  actualizarCategoria.cat_desp = cat_desp

  db.session.commit()
  return categoria_schema.jsonify(actualizarCategoria)

#DELETE############################################
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
  eliminarCategoria = Categoria.query.get(id)
  db.session.delete(eliminarCategoria)
  db.session.commit()
  return categoria_schema.jsonify(eliminarCategoria)


#Mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
  return jsonify({'Mensaje':'Bienvenido al tutorial API REST Python'})

if __name__ =="__main__":
  app.run(debug=True)