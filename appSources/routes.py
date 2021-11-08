from datetime import datetime
from flask import render_template
from appSources import app,mysql

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/testdb')
def testdb():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Utilisateur ''')
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('testdb.html',users=data,title='Test DataBase')