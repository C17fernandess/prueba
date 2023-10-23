from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db = SQLAlchemy(app)

class Usuarios(db.Model):
    __nombreTabla__ = 'usuarios'

    id = db.Column(db.Integer,primary_key=True) 
    nombre_usuario = db.Column(db.String(30),unique=True, nullable=False)
    correos_usuario = db.Column(db.ARRAY(db.String(30)),unique=True, nullable=False) 

    def json(self):
        return {'id' : id,'nombre_usuario' : self.nombre_usuario,'correos_usuario' : self.correos_usuario }

db.create_all()

@app.route('/usuarios', methods = ['POST'])
def CrearUsuario():
   try:
       data= request.get_json()
       usuario= Usuarios(nombre_usuario=data['nombre_usuario'],correos_usuario= data['correos_usuario'] )
       db.session.add(usuario)
       db.session.commit()
       return make_response(jsonify({'mensaje':'usuario creado'}),201)
   except Exception:
       return make_response(jsonify({'mensaje':'error creando el usuario'}),500)

@app.route('/usuarios', methods = ['GET'])
def ObtenerUsuarios():
   try:
       usuarios= Usuarios.query.all()
       if len(usuarios):
           return make_response(jsonify({'usuarios':[usuarios.json for usuario in usuarios]}),200)
       return make_response(jsonify({'mensaje':'usuarios no encontrados'}),404)     
   except Exception:
       return make_response(jsonify({'mensaje':'error obteniendo a los usuarios'}),500)

@app.route('/usuarios/<int:id>', methods = ['GET'])
def ObtenerUsuario(id):
   try:
       usuario= Usuarios.query.filter_by(id=id).first()
       return make_response(jsonify({'usuario':usuario.json()}),200)     
   except Exception:
       return make_response(jsonify({'mensaje':'usuario no encontrado'}),500)
   
@app.route('//usuarios/<int:id>', methods = ['PUT'])
def ActualizarUsuario(id):
   try:
       usuario= Usuarios.query.filter_by(id=id).first()
       if usuario:
        data= request.get_json()
        usuario.nombre_usuario = data['nombre_usuario']
        usuario.correos_usuario = data['correos_usuario']
        db.session.commit()
        return make_response(jsonify({'mensaje':'usuario actualizado'}),200)
       return make_response(jsonify({'mensaje':'usuario no encontrado'}),404)

   except Exception:
       return make_response(jsonify({'mensaje':'error actualizando el usuario'}),500)

if __name__=='__main__':
    app.run(debug=True)