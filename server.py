from flask import Flask, render_template, request, redirect, jsonify # jsonify lets us send JSON back!
# Import MySQLConnector class from mysqlconnection.py
from mysqlconnection import MySQLConnection
app = Flask(__name__)
'''
Set variable 'mysql' to be an instance of the MySQLConnector class,
taking our entire application as the first argument and the database
name as the second argument.
'''
mysql = MySQLConnection(app, 'notes')
#  HTML-oriented index method
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getall')
def getall():
    notes = mysql.query_db("SELECT * FROM notes")
    return render_template('notes.html', notes=notes)

# create new note
@app.route('/create', methods=['POST'])
def create():
    mysql.query_db("INSERT INTO notes(title, description, created_at, updated_at) VALUES('{}','{}', NOW(), NOW())".format(request.form['title'], request.form['description']))
    notes = mysql.query_db("SELECT * FROM notes")
    return render_template('notes.html', notes=notes)

@app.route('/update', methods=['POST'])
def update():
    mysql.query_db("UPDATE notes SET title = '{}', description = '{}', updated_at=NOW() WHERE id='{}'".format(request.form['title'], request.form['description'], request.form['id']))
    notes = mysql.query_db("SELECT * FROM notes")
    return render_template('notes.html', notes=notes)

@app.route('/delete', methods=['POST'])
def delete():
    mysql.query_db("DELETE FROM notes WHERE id='{}'".format(request.form['id']))
    notes = mysql.query_db("SELECT * FROM notes")
    return render_template('notes.html', notes=notes)

#  JSON-oriented index method
@app.route('/json')
def json():
    notes = mysql.query_db("SELECT * FROM notes")
    return jsonify(notes=notes)
#  For now, that's all we need
app.run(debug=True)