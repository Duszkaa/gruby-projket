from flask import Flask, render_template, url_for, request, g, redirect

from marshmallow import Schema,fields
import sqlite3

class TodoSchema(Schema):
    id = fields.Integer()
    czynnosc = fields.String()
    opis_czynnosci = fields.String()
    priorytet = fields.String()
    data = fields.String()
    godzina = fields.String()

todo_schema = TodoSchema()

def get_db():
    if not hasattr(g,'database'):
        conn = sqlite3.connect("./database.db")
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db


def close_db(error):
    if hasattr(g,'database'):
        g.sqlite_db.close()