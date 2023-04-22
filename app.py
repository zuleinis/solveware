#this is Bryan's branch
from flask import Flask, request, render_template
import db

# from models import InterfazUsuario
# from pymongo import MongoClient

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        # getting input with name = fname in HTML form
       nombre = request.form.get("nombre")
       
       db.db.test1.insert_one({"nombre" : nombre})
       
    return render_template('formulario.html')

# def test():
    
#     modelo_reporte = {
#     "numero_reporte": None,
#     "estado": "abierto",
#     "datos": {
#         "usuario": None,
#         "descripcion": None,
#         "tecnico": None
#     }
# }
    
#     # Create collection
#     db.db.test.insert_one(modelo_reporte)
    
#     # find rows in collection that meets condition
#     for user in db.db.test.find({"estado": "abierto"}):
#         print(user)
#     return "Connected to the data base!"

if __name__ == '__main__':
    app.run(debug=True)
