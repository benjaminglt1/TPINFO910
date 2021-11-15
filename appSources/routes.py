from datetime import datetime
from flask import render_template
from flask import request as reqform
from werkzeug.wrappers import request
from appSources import app,mysql
from .forms import LoginForm


@app.route('/')
def connexion():    
    return render_template('connexion.html',title='Connexion',year=datetime.now().year)
         
@app.route('/accueil',methods = ['POST'])
def accueil():
    global user
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Jeu ''')
    jeux = cursor.fetchall()
    
    res = reqform.form
    cursor = mysql.connection.cursor()
    query = ("SELECT * FROM Utilisateur WHERE Login=%s")
    data = (res['login'],)
    cursor.execute(query,data)
    user = cursor.fetchall()

    if user[0][6] != res['password']:
        print("!!!!!!!!!!Nok!!!!!!!!!!!")
        connexion()
    #cursor.execute(''' SELECT * FROM Utilisateur LIMIT 1 ''')# TODO : Mettre la WHERE clause pour prendre la valeur du formulaire envoyé par connexion
    #user = cursor.fetchall()

    cursor.close()
    return render_template('index.html',title='Accueil',year=datetime.now().year,jeux=jeux)

@app.route('/mesJeux')
def mesJeux():
    cursor = mysql.connection.cursor()
    query = ("SELECT * FROM Jeux_Utilisateur WHERE IdUtilisateur=%s")
    data = (user[0][0],)
    cursor.execute(query,data)
    idjeux = cursor.fetchall()
    #boucle pour récup chaque jeu avec son id ou JOIN dans la requête
    cursor.close()
    return render_template('mesJeux.html',title='Liste de mes jeux',year=datetime.now().year, jeux=jeux)

@app.route('/panier')
def panier():
    return render_template('panier.html',title='Mon panier',year=datetime.now().year)

@app.route('/listeJeux')
def listeJeux():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Categorie ''')
    categories = cursor.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Jeu ''')
    jeux = cursor.fetchall()
    cursor.close()
    return render_template('listeJeux.html',title='Liste de tous les jeux',year=datetime.now().year,jeux=jeux,categories=categories)

@app.route('/contact')
def contact():
    return render_template('contact.html',title='Contact',year=datetime.now().year)

@app.route('/pageJeu<string:idJeu>')
def pageJeu(idJeu):
    cursor = mysql.connection.cursor()
    query = ("SELECT * FROM Jeu WHERE IdJeu=%s")
    data = (idJeu)
    cursor.execute(query,data)
    jeu = cursor.fetchall()

    query = ("SELECT * FROM Editeur WHERE Id=%s")
    data = (jeu[4])
    cursor.execute(query,data)
    editeur = cursor.fetchall()

    query = ("SELECT * FROM Utilisateur_Jeux WHERE IdUtilisateur=%s AND IdJeu=%s")
    data = (user[0][0],idJeu)
    cursor.execute(query,data)
    tmp = cursor.fetchall()
    achetable = True
    if(tmp[0]):
        achetable = False

    cursor.close()
    return render_template('pageJeu.html',title='Page d\'un jeu',year=datetime.now().year,jeu=jeu,editeur=editeur,achetable=achetable)

@app.route('/jeuxCategorie/<string:categorie>')
def jeuxCategorie(categorie):
    cursor = mysql.connection.cursor()
    query = ("SELECT * FROM Jeu WHERE IdCategorie=%s")
    data = (categorie)
    cursor.execute(query,data)
    jeux = cursor.fetchall()
    cursor.close()
    return render_template('jeuxCategorie.html',title='Jeux par categorie',year=datetime.now().year,jeux=jeux)