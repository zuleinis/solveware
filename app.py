# Define tus rutas de Flask

from flask import Flask, render_template
from models import InterfazUsuario
# from pymongo import MongoClient

app = Flask(__name__)

# Crear una conexión a la base de datos
# client = MongoClient("<MongoDB URI>")
# db = client.databaseName
# collection = db.collectionName

@app.route('/')
def home():
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
