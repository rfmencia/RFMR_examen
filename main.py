#Diplomado FullStack V3 USIP
#Roger Fernando Mencia Rojas

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/admin_user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    cedula_identidad = db.Column(db.String(20))
    nombre = db.Column(db.String(100))
    primer_apellido = db.Column(db.String(100))
    segundo_apellido = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)

    def __init__(self, cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento):
        self.cedula_identidad = cedula_identidad
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.fecha_nacimiento = fecha_nacimiento

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(
        cedula_identidad=data['cedula_identidad'],
        nombre=data['nombre'],
        primer_apellido=data['primer_apellido'],
        segundo_apellido=data['segundo_apellido'],
        fecha_nacimiento=data['fecha_nacimiento']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{'id_usuario': u.id_usuario, 'cedula_identidad': u.cedula_identidad,
                      'nombre': u.nombre, 'primer_apellido': u.primer_apellido,
                      'segundo_apellido': u.segundo_apellido, 'fecha_nacimiento': u.fecha_nacimiento.isoformat()}
                     for u in usuarios]
    return jsonify(usuarios_json)

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        usuario_json = {'id_usuario': usuario.id_usuario, 'cedula_identidad': usuario.cedula_identidad,
                        'nombre': usuario.nombre, 'primer_apellido': usuario.primer_apellido,
                        'segundo_apellido': usuario.segundo_apellido, 'fecha_nacimiento': usuario.fecha_nacimiento.isoformat()}
        return jsonify(usuario_json)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        data = request.get_json()
        usuario.cedula_identidad = data.get('cedula_identidad', usuario.cedula_identidad)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.primer_apellido = data.get('primer_apellido', usuario.primer_apellido)
        usuario.segundo_apellido = data.get('segundo_apellido', usuario.segundo_apellido)
        usuario.fecha_nacimiento = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario actualizado'})
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario eliminado'})
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/usuarios/promedio-edad', methods=['GET'])
def promedio_edad():
    promedio = db.session.execute(text("SELECT AVG(EXTRACT(YEAR FROM AGE(NOW(), fecha_nacimiento))) AS promedio_edades FROM usuario")).scalar()
    return jsonify({'promedioEdad': promedio})

@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({'nameSystem': 'api-users', 'version': '1.0', 'developer':'Roger Fernando Mencia Rojas','email': 'rfmencia@gmail.com'})

if __name__ == '__main__':
    app.run()
