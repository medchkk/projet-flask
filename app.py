from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la connexion MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Remplace par l'adresse de ton serveur MySQL si nécessaire
app.config['MYSQL_USER'] = 'root'  # Ton utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'mohamed-1234'  # Ton mot de passe MySQL
app.config['MYSQL_DB'] = 'formulaireDB'  # Le nom de ta base de données

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        ville = request.form['ville']
        email = request.form['email']
        telephone = request.form['telephone']
        
        # Créer un curseur pour interagir avec la base de données
        cur = mysql.connection.cursor()
        
        # Insérer les données dans la base de données
        cur.execute("""
            INSERT INTO utilisateurs (nom, prenom, ville, email, telephone) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, prenom, ville, email, telephone))
        
        # Valider la transaction et fermer le curseur
        mysql.connection.commit()
        cur.close()

        return f"Merci {prenom} {nom}, nous avons bien reçu vos informations!"

    return render_template('index.html')

@app.route('/utilisateurs', methods=['GET'])
def afficher_utilisateurs():
    # Créer un curseur pour interagir avec la base de données
    cur = mysql.connection.cursor()

    # Récupérer tous les utilisateurs de la table
    cur.execute("SELECT * FROM utilisateurs")
    utilisateurs = cur.fetchall()

    # Fermer le curseur
    cur.close()

    # Rendre la page d'affichage avec les utilisateurs récupérés
    return render_template('utilisateurs.html', utilisateurs=utilisateurs)

if __name__ == '__main__':
    app.run(debug=True)
