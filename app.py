from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__) # Crear una instancia de la aplicación Flask
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL') # Configurar la URI de la base de datos desde la variable de entorno 'DB_URL'
db = SQLAlchemy(app) # Crear una instancia de SQLAlchemy y asociarla a la aplicación

# Crear la tabla en la base de datos utilizando el modelo Directory
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    emails = db.Column(db.ARRAY(db.String), nullable=False)

    def serialize(self):
         return {
            'id': self.id,
            'name': self.name,
            'emails': list(self.emails)
        }

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Endpoint de estado
@app.route('/status/', methods=['GET'])
def get_status():
    return make_response(jsonify({'message:':'pong'}),200)

# Endpoint para listar todos los directorios
@app.route('/directories', methods=['GET'])
def get_directories():
    directories = Directory.query.all()
    serialized_directories = [directory.serialize() for directory in directories]
    response = jsonify(serialized_directories)
    return make_response(response, 200)

# Endpoint para crear un directorio
@app.route('/directories', methods=['POST'])
def create_directory():
    data = request.get_json()
    name = data.get('name')
    emails = data.get('emails')
       
    # Intenta crear un nuevo directorio
    directory = Directory(name=name, emails=emails)
    try:
        db.session.add(directory)
        db.session.commit()
        response = jsonify(directory.serialize())
        return make_response(response, 201)
    except:
        db.session.rollback()
        response = jsonify({'message': 'Error: Ya existe un directorio con esos datos'})
        return make_response(response, 400) 

