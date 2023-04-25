#this is Bryan's branch
from flask import Flask, request, redirect, render_template, jsonify
from bson.objectid import ObjectId
from datetime import date, datetime
import db



# from models import InterfazUsuario
# from pymongo import MongoClient

app = Flask(__name__,template_folder='templates', static_folder='static')

@app.route('/')
def homepage():
    return render_template('index.html', title='Solveware')

#Collects data from the form and inserts it to the Database
@app.route('/crear-reporte', methods =["GET", "POST"])
def crear_reporte():
    if request.method == "POST":
        # getting input with name = fname in HTML form
       nombre = request.form.get("nombre")
       email = request.form.get("email")
       equipo = request.form.get("equipo")
       falla = request.form.get("falla")
       tel = request.form.get("tel")
       
       
       today = date.today()
       postdate = today.strftime("%Y-%m-%d")
       
       now = datetime.now()
       current_time = now.strftime("%H:%M:%S")
       
       db.db.test1.insert_one({"nombre" : nombre,
                               "email" : email,
                               "tel": tel,
                               "equipo": equipo,
                               "falla": falla,
                               "status": "abierto",
                               "postdate":postdate,
                               "posttime": current_time,
                               "closeddate": "Not yet closed",
                               "closedtime": "Not yet closed",
                               "tecnico": "Not yet assigned",
                               "fixstatus": "",
                               "descripción": ""})
       
    return render_template('formulario.html')

#Display all reports in the Database
@app.route('/display-reportes', methods =["GET"])
def showdata():
    reportes = db.db.test1.find().sort("_id", -1)
    
    #reportes = db.db.test1.find({"postdate": {'$regex': "April"}})
    #reportes = db.db.test1.find({'$and' : [{"postdate": {'$regex': "April"}},{"postdate": {'$regex': "2022"}}]})
    
    print(reportes)
    return render_template('reportes.html',title='Solveware',reportes=reportes)

#Display all reports in the database from the given month and year
@app.route('/display-reportes-por-mes-y-año', methods =["GET","POST"])
def showdatapermonth():
    month = ""
    year = ""
    
    if request.method == "POST":
        month = str(request.form.get("selected_month"))
        year = str(request.form.get("selected_year"))
    
    date = [month,year]
    regexdate = f"{year}-{month}"
    print(regexdate)
    #reportes = db.db.test1.find({'$and' : [{"postdate": {'$regex': month}},{"postdate": {'$regex': year}}]}).sort("_id", -1)
    reportes = db.db.test1.find({"postdate": {'$regex': regexdate}})
    print(reportes)
    #reportes = db.db.test1.find({'$and' : [{"postdate": {'$regex': "April"}},{"postdate": {'$regex': "2022"}}]})
    return render_template('reportes_por_mes_y_año.html',title='Solveware',reportes=reportes,date=date)

#Display specific report and assign tecnico
@app.route('/reporte-num-<id>',methods =["GET","POST"])
def showdatafrom(id):
    ObjId = ObjectId(str(id))
    reporte = db.db.test1.find({'_id' : ObjId})
    
    if request.method == "POST":
        tecnico = request.form.get("tecnicos")
        db.db.test1.update_one({'_id' : ObjId}, {'$set': {'tecnico': tecnico }})
        db.db.test1.update_one({'_id' : ObjId}, {'$set': {'status': "en ejecución" }})
    
    return render_template('reporte.html',title='Solveware', reporte=reporte)


#Deletes specific report
@app.route('/delete-<id>')
def deletedatafrom(id):
    ObjId = ObjectId(str(id))
    db.db.test1.delete_one({'_id' : ObjId})
    return redirect('/display-reportes')

#Update specific report / Cerrar reporte
@app.route('/update-<id>')
def updatedatafrom(id):
    ObjId = ObjectId(str(id))
    
    today = date.today()
    postdate = today.strftime("%Y-%m-%d")
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'status': 'cerrado'}})
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'closeddate': postdate }})
    db.db.test1.update_one({'_id' : ObjId}, {'$set': {'closedtime': current_time}})
    return redirect(f'/reporte-num-{id}')

#Display most broken equipment
@app.route('/equipo-con-mas-fallas', methods =["GET","POST"])
def equipos_con_mas_fallas():
        
        #result = db.db.test1.aggregate(pipeline)
        # result = db.db.test1.aggregate(
        #     [
        #         {"$group": {"_id": "$equipo", "count": {"$sum": 1}}},
        #         {"$sort": {"count": -1}},
        #     {"$limit": 1}
        #     ]
        # )
        #default values
        start_month = "01"
        start_day = "01"
        start_year = "2023"
        
        end_month = "12"
        end_day = "31"
        end_year = "2023"
        
        if request.method == "POST":
            start_day = request.form.get("start_day")
            start_month =  request.form.get("start_month")
            start_year = request.form.get("start_year")
            
            end_day = request.form.get("end_day")
            end_month =  request.form.get("end_month")
            end_year = request.form.get("end_year")
            
        start_date = f"{start_year}-{start_month}-{start_day}"
        end_date = f"{end_year}-{end_month}-{end_day}"
        
        dates = [start_date,end_date]

        pipeline = [
            {
                "$match": {
                    "postdate": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$equipo",
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
        ]

        #If the result is a tie, display all tied attributes
        results = list(db.db.test1.aggregate(pipeline))
        if results:
            max_count = results[0]['count']
        else:
            max_count = 0

        
        result = [result for result in results if result['count'] == max_count]
        return render_template('equipomasfallasporfecha.html', title='Solveware', result=result,dates=dates)

#Display the name of the person with the most entries in a selected date
@app.route('/persona-con-mas-fallas', methods =["GET","POST"])
def persona_con_mas_fallas():
        
        #default values
        start_month = "01"
        start_day = "01"
        start_year = "2023"
        
        end_month = "12"
        end_day = "31"
        end_year = "2023"
        
        if request.method == "POST":
            start_day = request.form.get("start_day")
            start_month =  request.form.get("start_month")
            start_year = request.form.get("start_year")
            
            end_day = request.form.get("end_day")
            end_month =  request.form.get("end_month")
            end_year = request.form.get("end_year")
            
        start_date = f"{start_year}-{start_month}-{start_day}"
        end_date = f"{end_year}-{end_month}-{end_day}"
        
        dates = [start_date,end_date]

        pipeline = [
            {
                "$match": {
                    "postdate": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$nombre",
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
        ]

        #If the result is a tie, display all tied attributes
        results = list(db.db.test1.aggregate(pipeline))
        if results:
            max_count = results[0]['count']
        else:
            max_count = 0

        
        result = [result for result in results if result['count'] == max_count]
        
        return render_template('personamasfallas.html',title='Solveware',result=result,dates=dates)

@app.route('/fallas-por-periodo', methods =["GET","POST"])
def fallas_por_periodo():
        
        #default values
        start_month = "01"
        start_day = "01"
        start_year = "2023"
        
        end_month = "12"
        end_day = "31"
        end_year = "2023"
        
        if request.method == "POST":
            start_day = request.form.get("start_day")
            start_month =  request.form.get("start_month")
            start_year = request.form.get("start_year")
            
            end_day = request.form.get("end_day")
            end_month =  request.form.get("end_month")
            end_year = request.form.get("end_year")
            
        start_date = f"{start_year}-{start_month}-{start_day}"
        end_date = f"{end_year}-{end_month}-{end_day}"
        
        dates = [start_date,end_date]

        #If the result is a tie, display all tied attributes
        result = db.db.test1.find({'$and': [{'postdate': {'$gte': start_date}}, {'closeddate': {'$lte': end_date}}]})
        print(result)
        
        count = 0
        for report in result:
            count += 1
            
        print(count)
            
        # results_count = results.count()
        # return f'The number of reports submitted between {start_date} and {end_date} is {results}'
        # if results:
        #     max_count = results[0]['count']
        # else:
        #     max_count = 0

        
        # result = [result for result in results if result['count'] == max_count]
        
        return render_template('promedioreportes.html',title='Solveware',result=count,dates=dates)

if __name__ == '__main__':
    app.run(debug=True)
