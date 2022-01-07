from datetime import datetime
from flask import render_template,redirect,url_for
from flask import request as reqform
from werkzeug.wrappers import request
from appSources import app,mysql
from .forms import LoginForm
import requests
import json

user=None

@app.route('/')
def connexion():    
    return render_template('connexion.html',title='Connexion',year=datetime.now().year)
         
@app.route('/accueil',methods = ['POST'])
def accueil():
    global user
    global alljeux
    if(user == None):  
        res = reqform.form
        cursor = mysql.connection.cursor()
        query = ("SELECT * FROM Utilisateur WHERE Login=%s")
        data = (res['login'],)
        cursor.execute(query,data)
        user = cursor.fetchall()

        if user[0][6] != res['password']:
            connexion()

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Jeu ORDER BY RAND() LIMIT 5 ''')
    jeux = cursor.fetchall()
    alljeux=jeux
    cursor.close()
    return render_template('index.html',title='Accueil',year=datetime.now().year,jeux=jeux)

@app.route('/mesJeux')
def mesJeux():
    global mesjeux
    cursor = mysql.connection.cursor()
    query = ("SELECT Jeu.Nom,Jeu.Description FROM Jeux_Utilisateur INNER JOIN Jeu ON Jeux_Utilisateur.IdJeu=Jeu.Id WHERE Jeux_Utilisateur.IdUtilisateur=%s")
    data = (user[0][0],)
    cursor.execute(query,data)
    jeux = cursor.fetchall()
    mesjeux=jeux
    cursor.close()
    return render_template('mesJeux.html',title='Liste de mes jeux',year=datetime.now().year, jeux=jeux)

@app.route('/panier')
def panier():
    global jeuxpanier
    global total
    cursor = mysql.connection.cursor()
    query = ("SELECT Jeu.Nom,Jeu.Prix,Jeu.Id FROM Panier INNER JOIN Panier_Utilisateur ON Panier.Id=Panier_Utilisateur.IdPanier INNER JOIN Jeu ON Panier_Utilisateur.IdJeu=Jeu.Id WHERE Panier.IdUtilisateur=%s")
    data = (user[0][0],)
    cursor.execute(query,data)
    jeux = cursor.fetchall()
    jeuxpanier=jeux
    cursor.close()

    total = 0
    for jeu in jeuxpanier:
        total = total + jeu[1]


    return render_template('panier.html',title='Mon panier',year=datetime.now().year,jeux=jeux,total=total)

@app.route('/listeJeux')
def listeJeux():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Categorie ''')
    categories = cursor.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Jeu''')
    jeux = cursor.fetchall()
    cursor.close()
    return render_template('listeJeux.html',title='Liste de tous les jeux',year=datetime.now().year,jeux=jeux,categories=categories)

@app.route('/contact')
def contact():
    coordonnees = []
    coordonnees.append("support@contact.fr")
    coordonnees.append("0601020304")
    return render_template('contact.html',title='Contact',year=datetime.now().year,coordonnees=coordonnees,valide=False)

@app.route('/contactForm',methods = ['POST'])
def contactForm():
    coordonnees = []
    coordonnees.append("support@contact.fr")
    coordonnees.append("0601020304")
    return render_template('contact.html',title='Contact',year=datetime.now().year,coordonnees=coordonnees,valide=True)


@app.route('/pageJeu/<string:idJeu>')
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
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM Categorie ''')
    categories = cursor.fetchall()
    cursor.close()
    return render_template('jeuxCategorie.html',title='Jeux par categorie',year=datetime.now().year,jeux=jeux,categories=categories)

@app.route('/payement',methods = ['POST'])
def payement():
    res = reqform.form
    
    montant = total
    url = 'http://api:8080/makeOperation'
    myobj = {"numero": str(res['numero']),"montant": montant}
    
    
    x = requests.post(url, json=myobj)
    
    rep = str(x.text).split("\\")
    res = rep[3].split("\"")

    
    if res[1] == "valide":
        op = "La transaction est valide. Les jeux ont été ajoutés à votre bibiliothèque"
        cursor = mysql.connection.cursor()
        querydel = ("DELETE Panier_Utilisateur FROM Panier_Utilisateur INNER JOIN Panier ON Panier_Utilisateur.IdPanier=Panier.Id WHERE Panier.IdUtilisateur=%s AND Panier_Utilisateur.IdJeu=%s")
        queryins = ("INSERT INTO Jeux_Utilisateur(IdUtilisateur,IdJeu) VALUES (%s,%s)")
        for j in jeuxpanier:
            data = (user[0][0],j[2])
            cursor.execute(querydel,data)
            cursor.execute(queryins,data)

        cursor.close()
        mysql.connection.commit()
    else:
        op = "La transaction n'est pas valide"
    
    

    return render_template('paiement.html',title='Paiement',year=datetime.now().year,op=op)


@app.route('/ajoutPanier',methods = ['POST'])
def ajoutPanier():
    res = reqform.form
    

    cursor = mysql.connection.cursor()
    queryins = ("INSERT INTO Panier_Utilisateur(Id,IdPanier,IdJeu) VALUES (NULL,%s,%s)")
    
    idjeu = int(res['idjeu'])
    data = (user[0][0],idjeu)
    cursor.execute(queryins,data)

    cursor.close()
    mysql.connection.commit()
    #test = ""+str(res)+"  -  "+str(idjeu)
    return redirect(url_for('panier'))
    #return render_template('test.html',test=test)