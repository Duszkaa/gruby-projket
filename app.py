from datetime import date

from flask import Flask, render_template, url_for, request, g, redirect
import sqlite3

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
# cursor.execute("insert into transakcje (waluta,kwota,user) values (?,?,?)", ('zl','300','Marcin'))

connection.commit()
connection.close()

def get_db():
    if not hasattr(g,'database'):
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'database'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__name__":
    app.run(debug=True)
