from colorama import Cursor
from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():

    sql = "SELECT * FROM `persons`;"
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    persons=cursor.fetchall()
    print(persons)
    conn.commit()
    return render_template('persons/index.html', persons=persons)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM persons WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM persons WHERE id=%s",(id))
    persons=cursor.fetchall()
    conn.commit()
    return render_template('persons/edit.html', persons=persons)


@app.route('/create')
def create():
    return render_template('persons/create.html')

@app.route('/store', methods=['POST'])
def storage():

    _name=request.form['txtName']
    _fi_surname=request.form['txtFisurname']
    _se_surname=request.form['txtSesurname']
    _address=request.form['txtAddress']
    _add_num=request.form['txtAddNum']
    _district=request.form['txtDistrict']
    _phone_num=request.form['txtPhone1']
    _phone_num2=request.form['txtPhone2']
        
    sql = "INSERT INTO `persons` (`id`,  `name`, `fi_surname`, `se_surname`, `address`, `add_num`, `district`, `phone_num`, `phone_num2`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);"

    datos = (_name,_fi_surname,_se_surname,_address,_add_num,_district,_phone_num,_phone_num2)

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('persons/index.html')  

if __name__ == '__main__':
    app.run(debug=True)