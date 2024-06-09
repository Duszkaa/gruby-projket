from datetime import datetime
from flask import Flask, render_template, url_for, request, g, redirect, jsonify
from marshmallow import Schema,fields
import sqlite3
from database import TodoSchema, todo_schema, get_db, close_db
import mysql.connector


app = Flask(__name__)

try:
    mydb = mysql.connector.connect(host="6187AZ.mysql.pythonanywhere-services.com", user="6187AZ", password="haslo123", database="6187AZ$default")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT *FROM TODO")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    print("dziala")
except:
    print("nie dziala")
    mydb = None




# caly JSON
@app.route('/api/czynnosci', methods = ["GET", "POST"])
def get_czynnosci():
    dbcursor = mydb.cursor(dictionary=True)
    if request.method == "GET":
        sql_command = "select * from TODO"
        dbcursor.execute(sql_command)
        czynnosci = dbcursor.fetchall()
        todo_schema = TodoSchema(many=True)

        return jsonify({
            "success": True,
            "dane": todo_schema.dump(czynnosci)
        })

    elif request.method == "POST":
        dane = request.json
        if "priorytet" or "czynnosc" or "opis_czynnosci" or "godzina" or "data" not in dane:
             return  jsonify({
                 "succes": False,
                 "eror": "Please prvide all required information"
             }),440
        else:
            dbcursor = mydb.cursor()
            sql_command = "insert into TODO(czynnosc, opis_czynnosci, priorytet, data, godzina) values(%s, %s, %s, %s, %s);"
            dbcursor.execute(sql_command, [dane["czynnosc"], dane["opis_czynnosci"], dane["priorytet"], dane["data"], dane["godzina"]])
            mydb.commit()
            return jsonify({
                "success": True,
                "info": "Dane dodane poprawnie"
            }),201

#funkcja sprawdzajaca czy w zadaniu jest poprawnie wpisana data
def isDate(zmienna):
    format = "%d-%m-%Y"
    try:
        res = bool(datetime.strptime(zmienna, format))
        return True
    except ValueError:
        return False

#funkcja sprawdzajaca czy w zadaniu jest poprawnie wpisana godzina
def isTime(zmienna):
    for fmt in ('%H:%M:%S.%f', '%H:%M:%S'):
        try:
            datetime.strptime(zmienna, fmt)
            return True
        except ValueError:
            continue
    return False

# Json z metoda PUT, DELETE i GET z wyszukiwaniem przez id
@app.route('/api/czynnosci/<int:id>', methods = ["GET","PUT","DELETE"])
def get_czynnosci_id(id):
    # db = get_db()
    dbcursor = mydb.cursor(dictionary=True)
    sql_command = "select * from TODO where id = %s"
    if request.method == "GET":
        dbcursor.execute(sql_command, [id])
        czynnosci = dbcursor.fetchone()
        todo_schema = TodoSchema(many=False)
        return jsonify({
            "success": True,
            "data": todo_schema.dump(czynnosci)
        }),200

    else:
        if request.method == 'PUT':
            dane = request.json
            dbcursor.execute(sql_command, [id])
            todo_schema = TodoSchema(many=False)
            changed_dana = dbcursor.fetchone()
            changed_dana = todo_schema.dump(changed_dana)
            czynnosc = changed_dana['czynnosc']
            data = changed_dana['data']
            godzina = changed_dana['godzina']
            opis_czynnosci = changed_dana['opis_czynnosci']
            priorytet = changed_dana['priorytet']
            for x in dane:
                if x == 'czynnosc':
                    czynnosc = dane.get(x)
                elif x == "data":
                    data = dane.get(x)
                elif x == "godzina":
                    godzina = dane.get(x)
                elif x == "opis_czynnosci":
                    opis_czynnosci = dane.get(x)
                elif x == "priorytet":
                    priorytet = dane.get(x)
            if priorytet == "medium" or priorytet == "low" or priorytet == "high":
                sql_command = "UPDATE TODO SET czynnosc = %s, data = %s, godzina = %s, opis_czynnosci = %s, priorytet = %s where id = %s;"
                dbcursor.execute(sql_command, [czynnosc, data, godzina, opis_czynnosci, priorytet, id])
                mydb.commit()
                return jsonify(
                    {"success": True,
                    "info": "Dane zmienione"}
                ), 200
            else:
                return jsonify(
                {"success": False,
                 "info": "Dane wpisane niepoprawnie"}
                ), 400

        if request.method == 'DELETE':
            sql_command = "DELETE FROM TODO WHERE id= %s;"
            dbcursor.execute(sql_command, [id])
            mydb.commit()
            return jsonify({
                "success": True,
                "info": "Dane usunięte"
            }),201



# strona glowna
@app.route('/add', methods = ["GET", "POST"])
def add():
    dbcursor = mydb.cursor(dictionary=True)
    sql_command = "select * from TODO;"
    dbcursor.execute(sql_command)
    TODO = dbcursor.fetchall()

    if request.method == "GET":
        return render_template("add.html", TODO = TODO)
    else:
        fCzynnosc = request.form['fCzynnosc']
        fOpis = request.form['fOpis']
        fPriorytet = request.form['fPriorytet']
        fData = request.form['fData']
        fGodzina  = request.form['fGodzina']

        if fCzynnosc != "" and fOpis != "" and fData != "" and fGodzina != "":
            sql_command = "insert into TODO(czynnosc, opis_czynnosci, priorytet, data, godzina) values(%s, %s, %s, %s, %s);"
            dbcursor.execute(sql_command, [fCzynnosc, fOpis, fPriorytet, fData, fGodzina])
            mydb.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('add'))

@app.route('/update/<int:id>', methods = ["GET", "POST"])
def update(id):
    dbcursor = mydb.cursor(dictionary=True)
    sql_command = "select * from TODO where id = %s"
    dbcursor.execute(sql_command, [id])
    TODO = dbcursor.fetchone()

    if request.method == "GET":
        return render_template("update.html", TODO = TODO)

    if request.method == "POST":
        fCzynnosc = request.form['fCzynnosc']
        fOpis = request.form['fOpis']
        fPriorytet = request.form['fPriorytet']
        fData = request.form['fData']
        fGodzina  = request.form['fGodzina']

        if fCzynnosc != "" and fOpis != "" and fData != "" and fGodzina != "":
            sql_command = "update TODO set czynnosc = %s, opis_czynnosci = %s, priorytet = %s, data = %s, godzina = %s where id = %s;"
            dbcursor.execute(sql_command, [fCzynnosc, fOpis, fPriorytet, fData, fGodzina, id])
            mydb.commit()
            return redirect(url_for('index'))
        else:
            return render_template("update.html", TODO = TODO)


# strona glowna
@app.route('/')
def index():
    dbcursor = mydb.cursor(dictionary=True)
    sql_command = "select * from TODO;"
    dbcursor.execute(sql_command)
    TODO = dbcursor.fetchall()

    return render_template("show.html", TODO = TODO)

@app.route('/delete/<int:id>')
def delete(id):
    sql_command = "delete from TODO where id=%s"
    dbcursor = mydb.cursor(dictionary=True)
    dbcursor.execute(sql_command, [id])
    mydb.commit()

    return redirect(url_for('index'))



# strona API
@app.route('/api')
def api():
    return render_template("api.html")



if __name__ == "__name__":
    app.run(debug=True)