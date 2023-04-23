#this is Bryan's branch
from flask import Flask, request, redirect, render_template
from datetime import date, datetime
import db



# from models import InterfazUsuario
# from pymongo import MongoClient

app = Flask(__name__)

#Collects data from the form and inserts it to the Database
@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        # getting input with name = fname in HTML form
       nombre = request.form.get("nombre")
       email = request.form.get("email")
       equipo = request.form.get("equipo")
       falla = request.form.get("falla")
       
       
       today = date.today()
       postdate = today.strftime("%B %d, %Y")
       
       now = datetime.now()
       current_time = now.strftime("%H:%M:%S")
       
       db.db.test1.insert_one({"nombre" : nombre,
                               "email" : email,
                               "equipo": equipo,
                               "falla": falla,
                               "status": "abierto",
                               "postdate":postdate,
                               "posttime": current_time})
       
    return render_template('formulario.html')

#Display all reports in the Database
@app.route('/display', methods =["GET"])
def showdata():
    reportes = db.db.test1.find()
    print(reportes)
    return render_template('index.html',reportes=reportes)

#Display specific report
@app.route('/display-<name>')
def showdatafrom(name):
    reporte = db.db.test1.find({"nombre":name})
    
    return render_template('reporte.html',reporte=reporte)

#Deletes specific report
@app.route('/delete-<name>')
def deletedatafrom(name):
    db.db.test1.delete_one({"nombre":name})
    return redirect('/display')

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
