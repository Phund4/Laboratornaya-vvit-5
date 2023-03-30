import requests
from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="ph159753da",
                        host="localhost",
                        port="5432")


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


cursor = conn.cursor()


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return render_template('login.html', Error="Пустой логин или пароль")
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if len(records) > 0:
        return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
    else:
        return render_template('login.html', Error="Пользователя нет в базе данных либо неверный логин или пароль")
