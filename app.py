from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Home",isi="Selamat Datang Di Web Kagaku No Hikari")

@app.route('/about')
def about(): 
    return render_template('about.html',title="About Me")

@app.route('/myproject')
def myproject() :
    return render_template('myproject.html',title="My project",isi="  My public Project's :")

if __name__ == '__main__' :
    app.run(debug=True)