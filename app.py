from flask import Flask, render_template, url_for, request, g, redirect, jsonify
from marshmallow import Schema,fields
import sqlite3
from database import TodoSchema, todo_schema, get_db, close_db


app = Flask(__name__)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute('''create table if not exists TODO (
                    id integer primary key autoincrement,
                    czynnosc varchar(60),
                    opis_czynnosci varchar(255),
                    priorytet varchar2(30),
                    data date not null default(date()),
                    godzina time
                    )''')

connection.commit()
connection.close()


# caly JSON
@app.route('/api/czynnosci', methods = ["GET", "POST"])
def get_czynnosci():
    db = get_db()

    if request.method == "GET":
        sql_command = "select * from TODO"
        cursor = db.execute(sql_command)
        czynnosci = cursor.fetchall()
        todo_schema = TodoSchema(many=True)

        return jsonify({
            "success": True,
            "dane": todo_schema.dump(czynnosci)
        })

    elif request.method == "POST":
        dane = request.json
        if "priorytet" not in dane:
             return  jsonify({
                 "succes": False,
                 "eror": "Please prvide all required information"
             }),440
        else:
            sql_command = "insert into TODO(czynnosc, opis_czynnosci, priorytet, data, godzina) values(?,?,?,?,?);"
            db.execute(sql_command, [dane["czynnosc"], dane["opis_czynnosci"], dane["priorytet"], dane["data"], dane["godzina"]])
            db.commit()
            return jsonify({
                "success": True,
                "info": "Transaction add successfuly"
            }),201


# Json z metoda PUT, DELETE i GET z wyszukiwaniem przez id
@app.route('/api/czynnosci/<int:id>', methods = ["GET","PUT","DELETE"])
def get_czynnosci_id(id):
    db = get_db()
    sql_command = "select * from TODO where id = ?"
    if request.method == "GET":
        cursor = db.execute(sql_command, [id])
        czynnosci = cursor.fetchone()
        todo_schema = TodoSchema(many=False)
        return jsonify({
            "success": True,
            "data": todo_schema.dump(czynnosci)
        }),200

    else:
        if request.method == 'PUT':
            dane = request.json
            cursor = db.execute(sql_command, [id])
            todo_schema = TodoSchema(many=False)
            changed_dana = cursor.fetchone()
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
            sql_command = "UPDATE TODO SET czynnosc = ?, data = ?, godzina = ?, opis_czynnosci = ?, priorytet = ? where id = ?;"
            db.execute(sql_command, [czynnosc, data, godzina, opis_czynnosci, priorytet, id])
            db.commit()
            return jsonify(
                {"success": True,
                 "info": "Dane zmienione"}
            ), 200

        if request.method == 'DELETE':
            sql_command = "DELETE FROM TODO WHERE id=?;"
            db.execute(sql_command,str(id))
            db.commit()
            return jsonify({
                "success": True,
                "info": "Delete zadzialal :)"
            }),201



# strona glowna
@app.route('/add', methods = ["GET", "POST"])
def add():
    db = get_db()
    sql_command = "select * from TODO;"
    cursor = db.execute(sql_command)
    TODO = cursor.fetchall()

    if request.method == "GET":
        return render_template("add.html", TODO = TODO)
    else:
        fCzynnosc = request.form['fCzynnosc']
        fOpis = request.form['fOpis']
        fPriorytet = request.form['fPriorytet']
        fData = request.form['fData']
        fGodzina  = request.form['fGodzina']

        if fCzynnosc != "" and fOpis != "" and fData != "" and fGodzina != "":
            db = get_db()
            sql_command = "insert into TODO(czynnosc, opis_czynnosci, priorytet, data, godzina) values(?,?,?,?,?);"
            db.execute(sql_command, [fCzynnosc, fOpis, fPriorytet, fData, fGodzina])
            db.commit()
            return redirect(url_for('add'))
        else:
            return redirect(url_for('add'))

@app.route('/update', methods = ["GET", "POST"])
def update():
    db = get_db()
    sql_command = "select * from TODO;"
    cursor = db.execute(sql_command)
    TODO = cursor.fetchall()

    if request.method == "GET":
        return render_template("update.html", TODO = TODO)
    else:
        fCzynnosc = request.form['fCzynnosc']
        fOpis = request.form['fOpis']
        fPriorytet = request.form['fPriorytet']
        fData = request.form['fData']
        fGodzina  = request.form['fGodzina']

        if fCzynnosc != "" and fOpis != "" and fData != "" and fGodzina != "":
            db = get_db()
            sql_command = "insert into TODO(czynnosc, opis_czynnosci, priorytet, data, godzina) values(?,?,?,?,?);"
            db.execute(sql_command, [fCzynnosc, fOpis, fPriorytet, fData, fGodzina])
            db.commit()
            return redirect(url_for('update'))
        else:
            return redirect(url_for('update'))


# strona wyswietl
@app.route('/wyswietl')
def wyswietl():
    db = get_db()
    sql_command = "select * from TODO;"
    cursor = db.execute(sql_command)
    TODO = cursor.fetchall()

    return render_template("show.html", TODO = TODO)




# strona index
@app.route('/')
def index():
    return render_template("index.html")


# strona API
@app.route('/api')
def api():
    return render_template("api.html")



if __name__ == "__name__":
    app.run(debug=True)