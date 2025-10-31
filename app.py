from flask import Flask, render_template, request , redirect, url_for,session
from flask_mysqldb import MySQL , MySQLdb
import bcrypt

app=Flask(__name__)
app.config['mysql_cursorclass']='DictCursor'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db_pemilu_osis'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin where username=%s',[username])
        cursor.close()
        admin=cursor.fetchone()
        
        return username
        
    return render_template('login.html')

@app.route('/seeder')
def seeder() :
    
    username="petugas"
    password="petugas123"
    nama="petugas baik hati"

    bytesPassword=password.encode('utf-8')
    hashed=bcrypt.gensalt()
    hashPassword=bcrypt.hashpw(bytesPassword,salt=hashed)

    cursor=mysql.connection.cursor()
    cursor.execute('INSERT IGNORE INTO admin (username,password,nama) VALUES (%s,%s,%s)',[username,hashPassword,nama])
    mysql.connection.commit()
    cursor.close()

    return "Data admin berhasil ditambahkan"
    
@app.route('/pemilu')
def pemilu():
    return render_template('pemilu/index.html')

@app.route('/kelas')
def kelas():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM kelas')
    data=cursor.fetchall()
    cursor.close()

    return render_template('kelas/index.html', data=data)



@app.route('/tambah_kelas', methods=['GET','POST'])
def tambah_kelas():
    if request.method=='POST':
        nama=request.form['kode_kelas']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO kelas (kode_kelas) VALUES (%s)', (nama,))
        mysql.connection.commit()
        cursor.close()
        return redirect (url_for('kelas'))
    return render_template('kelas/create.html')

@app.route('/edit_kelas/<int:id>', methods=['GET','POST'])
def edit_kelas(id):
    if request.method=='POST':
        nama=request.form['kode_kelas']
        cursor=mysql.connection.cursor()
        cursor.execute('UPDATE kelas SET kode_kelas=%s WHERE id_kelas=%s', (nama,id,))
        mysql.connection.commit()
        cursor.close()
        return redirect (url_for('kelas'))

    cnn=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cnn.execute('SELECT * FROM kelas WHERE id_kelas=%s',(id,))
    kelas=cnn.fetchone()
    cnn.close()
    return render_template('kelas/edit.html', data=kelas)

@app.route('/delete_kelas/<int:id>', methods=['POST','GET'])
def delete_kelas(id):
        cursor=mysql.connection.cursor()
        cursor.execute('DELETE FROM kelas WHERE id_kelas=%s',(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect (url_for('kelas'))

@app.route('/voters')
def voters():
    cnn=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cnn.execute("SELECT  voters.id_voter , voters.nama , kelas.kode_kelas from kelas JOIN voters ON voters.id_kelas = kelas.id_kelas") 
    data=cnn.fetchall()
    cnn.close()
    return render_template('voters/index.html', data=data)

@app.route('/tambah_voters',methods=['POST','GET'])
def tambah_voters():
    if request.method=='POST':
        nama=request.form['nama']
        id_kelas=request.form['id_kelas']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO voters (nama,id_kelas) values (%s,%s)",(nama,id_kelas))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('voters'))

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM kelas')
    kelas=cursor.fetchall()
    cursor.close()
    return render_template('voters/create.html',data=kelas)

@app.route('/edit_voters/<int:id>', methods=['GET','POST'])
def edit_voters(id):
    if request.method=='POST':
        nama=request.form['nama']
        id_kelas=request.form['id_kelas']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE voters SET nama=%s , id_kelas=%s WHERE id_voter=%s",(nama,id_kelas,id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('voters'))
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM voters where id_voter=%s",(id,))
    voters=cursor.fetchone()
    cursor.execute('SELECT * FROM  kelas')
    kelas=cursor.fetchall()
    cursor.close()
    return render_template('voters/edit.html', data=voters, data_kelas=kelas)

@app.route('/hapus_voters/<int:id>', methods=['POST','GET'])
def hapus_voters(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM voters WHERE id_voter=%s',(id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('voters'))

if __name__=='__main__':
    app.run(debug=True) 


