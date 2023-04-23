#this is Bryan's branch
from flask import Flask, request, redirect, render_template
from bson.objectid import ObjectId
from datetime import date, datetime
import db



# from models import InterfazUsuario
# from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

#Collects data from the form and inserts it to the Database
@app.route('/crear-reporte', methods =["GET", "POST"])
def crear_reporte():
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
                               "posttime": current_time,
                               "closeddate": "Not yet closed",
                               "closedtime": "Not yet closed",
                               "tecnico": "Not yet assigned",})
       
    return render_template('formulario.html')

#Display all reports in the Database
@app.route('/display-reportes', methods =["GET"])
def showdata():
    reportes = db.db.test1.find().sort("_id", -1)
    
    #reportes = db.db.test1.find({"postdate": {'$regex': "April"}})
    #reportes = db.db.test1.find({'$and' : [{"postdate": {'$regex': "April"}},{"postdate": {'$regex': "2022"}}]})
    
    print(reportes)
    return render_template('reportes.html',reportes=reportes)

#Display specific report
@app.route('/reporte-num-<id>',methods =["GET","POST"])
def showdatafrom(id):
    ObjId = ObjectId(str(id))
    reporte = db.db.test1.find({'_id' : ObjId})
    
    if request.method == "POST":
        tecnico = request.form.get("tecnicos")
        db.db.test1.update_one({'_id' : ObjId}, {'$set': {'tecnico': tecnico }})
        db.db.test1.update_one({'_id' : ObjId}, {'$set': {'status': "en progreso" }})
    
    return render_template('reporte.html',reporte=reporte)


#Deletes specific report
@app.route('/delete-<id>')
def deletedatafrom(id):
    ObjId = ObjectId(str(id))
    db.db.test1.delete_one({'_id' : ObjId})
    return redirect('/display')

#Update specific report / Cerrar reporte
@app.route('/update-<id>')
def updatedatafrom(id):
    ObjId = ObjectId(str(id))
    
    today = date.today()
    postdate = today.strftime("%B %d, %Y")
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'status': 'cerrado'}})
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'closeddate': postdate }})
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'closedtime': current_time}})
    return redirect(f'/reporte-num-{id}')

#Display most broken equipment
@app.route('/equipo-con-mas-fallas', methods =["GET"])
def equipos_con_mas_fallas():
        
        #result = db.db.test1.aggregate(pipeline)
        result = db.db.test1.aggregate(
            [
                {"$group": {"_id": "$equipo", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            {"$limit": 1}
            ]
        )
        
        return render_template('equipomasfallas.html',result=result)

if __name__ == '__main__':
    app.run(debug=True)
