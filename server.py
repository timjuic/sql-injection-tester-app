import re
from flask import Flask, render_template, request, send_from_directory
import sqlite3
import os
import json

app = Flask(__name__)


DATABASE = os.path.join(os.path.dirname(__file__), 'users.sqlite')

def create_users_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
   #  c.execute("DROP TABLE IF EXISTS Users")
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (username TEXT PRIMARY KEY,
                  firstname TEXT,
                  lastname TEXT,
                  email TEXT,
                  age INTEGER)''')
    conn.commit()
    conn.close()


create_users_table()


def insert_sample_data():
   conn = sqlite3.connect('users.sqlite')
   c = conn.cursor()
   
   c.execute("INSERT INTO Users VALUES ('test', 'Tester', 'Tester', 'test.test@test.com', 21)")
   c.execute("INSERT INTO Users VALUES ('pero123', 'Petar', 'Perić', 'petar.peric@example.com', 30)")
   c.execute("INSERT INTO Users VALUES ('iva456', 'Ivana', 'Ivić', 'ivana.ivic@example.com', 25)")
   c.execute("INSERT INTO Users VALUES ('marko789', 'Marko', 'Marković', 'marko.markovic@example.com', 35)")
   c.execute("INSERT INTO Users VALUES ('ana567', 'Ana', 'Anić', 'ana.anic@example.com', 28)")
   c.execute("INSERT INTO Users VALUES ('josip234', 'Josip', 'Josipović', 'josip.josipovic@example.com', 40)")
   c.execute("INSERT INTO Users VALUES ('maja345', 'Maja', 'Majić', 'maja.majic@example.com', 31)")
   c.execute("INSERT INTO Users VALUES ('petra987', 'Petra', 'Petrić', 'petra.petric@example.com', 27)")
   c.execute("INSERT INTO Users VALUES ('matko654', 'Matko', 'Matković', 'matko.matkovic@example.com', 33)")
   c.execute("INSERT INTO Users VALUES ('mateo123', 'Mateo', 'Matić', 'mateo.matic@example.com', 25)")
   c.execute("INSERT INTO Users VALUES ('ana321', 'Ana', 'Anić', 'ana.anic@example.com', 30)")
   c.execute("INSERT INTO Users VALUES ('filip456', 'Filip', 'Filipović', 'filip.filipovic@example.com', 27)")
   c.execute("INSERT INTO Users VALUES ('martina789', 'Martina', 'Martinović', 'martina.martinovic@example.com', 35)")
   c.execute("INSERT INTO Users VALUES ('ivan567', 'Ivan', 'Ivanić', 'ivan.ivanic@example.com', 28)")
   c.execute("INSERT INTO Users VALUES ('lena234', 'Lena', 'Lenić', 'lena.lenic@example.com', 40)")
   c.execute("INSERT INTO Users VALUES ('josip345', 'Josip', 'Josipović', 'josip.josipovic@example.com', 31)")
   c.execute("INSERT INTO Users VALUES ('nikolina987', 'Nikolina', 'Nikolić', 'nikolina.nikolic@example.com', 27)")
   c.execute("INSERT INTO Users VALUES ('dario654', 'Dario', 'Darić', 'dario.daric@example.com', 33)")
   c.execute("INSERT INTO Users VALUES ('josipjos', 'Josip', 'Josipović', 'josip.josipovic@example.com', 40)")
   c.execute("INSERT INTO Users VALUES ('maja.m', 'Maja', 'Majić', 'maja.majic@example.com', 31)")
   c.execute("INSERT INTO Users VALUES ('petra-p', 'Petra', 'Petrić', 'petra.petric@example.com', 27)")
   c.execute("INSERT INTO Users VALUES ('matko.m', 'Matko', 'Matković', 'matko.matkovic@example.com', 33)")
   c.execute("INSERT INTO Users VALUES ('ana.c', 'Ana', 'Cvitan', 'ana.cvitan@example.com', 28)")
   c.execute("INSERT INTO Users VALUES ('mario.k', 'Mario', 'Kovač', 'mario.kovac@example.com', 29)")
   c.execute("INSERT INTO Users VALUES ('tina.t', 'Tina', 'Tomić', 'tina.tomic@example.com', 26)")
   c.execute("INSERT INTO Users VALUES ('janko.j', 'Janko', 'Janković', 'janko.jankovic@example.com', 32)")
   c.execute("INSERT INTO Users VALUES ('lena.m', 'Lena', 'Marić', 'lena.maric@example.com', 30)")
    
   conn.commit()
   conn.close()

# insert_sample_data()


def get_all_users():
    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()

    c.execute("SELECT * FROM Users")
    rows = c.fetchall()

    users = []
    for row in rows:
        user = {
            'username': row[0],
            'firstname': row[1],
            'lastname': row[2],
            'email': row[3],
            'age': row[4],
        }
        users.append(user)

    conn.close()

    for user in users:
        print(user)

    return users

get_all_users()


def get_user_by_username(username):
    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()

    c.execute("SELECT * FROM Users WHERE username=?", (username,))
    row = c.fetchone()

    if not row:
        return None

    user = {
        'username': row[0],
        'firstname': row[1],
        'lastname': row[2],
        'email': row[3],
        'age': row[4],
    }

    conn.close()

    return user


@app.route('/')
def index():
    return render_template('index.html')



@app.route( '/static/<path:path>' )
def serve_static( path ):
    return send_from_directory('static', path)

@app.route('/pretrazi-parameterized', methods=['GET'])
def search_parameter():
    username = request.args.get('username')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("SELECT * FROM Users WHERE username = ?", (username,))
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            'username': row[0],
            'firstname': row[1],
            'lastname': row[2],
            'email': row[3],
            'age': row[4],
        })
        conn.close()
    return json.dumps(results)


def is_safe_string(string):
    pattern = re.compile(r'^[a-zA-Z0-9@_.-]*$')
    return bool(pattern.match(string))


@app.route('/pretrazi-pattern', methods=['GET'])
def search_pattern():
    username = request.args.get('username')
    if not is_safe_string(username):
        return json.dumps("sql injection detected")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("SELECT * FROM Users WHERE username = '" + username + "'")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            'username': row[0],
            'firstname': row[1],
            'lastname': row[2],
            'email': row[3],
            'age': row[4],
        })
    conn.close()
    return json.dumps(results)


@app.route('/pretrazi-vulnerable', methods=['GET'])
def search_vulnerable():
    username = request.args.get('username')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("SELECT * FROM Users WHERE username = '" + username + "'")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            'username': row[0],
            'firstname': row[1],
            'lastname': row[2],
            'email': row[3],
            'age': row[4],
        })
    conn.close()
    return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True)
