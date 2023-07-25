from flask import Flask, render_template, request, redirect, url_for
import os
import database as db
import pymysql

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)
DB_HOST = 'servidorwt.mysql.database.azure.com'
DB_USER = 'usermysql'
DB_PASSWORD = 'Softec2023wt'
DB_NAME = 'pag'

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('inicio.html', data=insertObject)

@app.route('/nueva_pagina', methods=['POST'])
def nueva_pagina():
    username = request.form['usuario']
    password = request.form['contrasena']
    cursor = db.database.cursor()
    consulta = "SELECT * FROM consumos where n_medidor = %s"
    cursor.execute(consulta,(username,))
    #cursor = db.database.cursor()
    #cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('consumo.html', data=insertObject)


'''@app.route('/nueva_pagina', methods=['POST'])
def nueva_pagina():
    username = request.form['usuario']
    password = request.form['contrasena']
    cursor = db.database.cursor()
    consulta = "SELECT * FROM users where username = %s and name = %s"
    cursor.execute(consulta,(username,password,))
    #cursor = db.database.cursor()
    #cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('consumo.html', data=insertObject)
'''

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)




@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)


    