from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

with open("dictionnaire.txt", "r", encoding="utf-8") as fichier:
    lignes = fichier.readlines()

mots = []

for ligne in lignes:
    mot = ligne.split(";")[0]
    mots.append(mot)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/play", methods=["POST"])
def play():
    nom = request.form.get("nom")
    lettre = request.form.get("lettre")

    # Nouveau jeu
    if nom:
        session["nom"] = nom

        mot_secret = random.choice(mots)
        session["mot_secret"] = mot_secret

        session["vies"] = 5
        session["potence"] = 0
        session["lettres_jouees"] = []

        mot_cache = "_" * len(mot_secret)
        session["mot_cache"] = mot_cache

    # Lettre choisie pendant le jeu
    else:
        nom = session["nom"]
        mot_secret = session["mot_secret"]
        mot_cache = session["mot_cache"]

        if lettre:

            # Vérifier si la lettre a déjà été jouée
            if lettre in session["lettres_jouees"]:
                return render_template(
                    "play.html",
                    nom=nom,
                    mot_secret=mot_secret,
                    mot_cache=mot_cache
                )

            # Ajouter la lettre à la liste des lettres jouées
            session["lettres_jouees"].append(lettre)

            if lettre in mot_secret:
                nouveau_cache = ""

                for i in range(len(mot_secret)):
                    if mot_secret[i] == lettre:
                        nouveau_cache += lettre
                    else:
                        nouveau_cache += mot_cache[i]

                mot_cache = nouveau_cache
                session["mot_cache"] = mot_cache

            else:
                session["vies"] -= 1
                session["potence"] += 1

                if session["vies"] == 0:
                    return render_template(
                        "gameover.html",
                        nom=nom,
                        mot_secret=mot_secret
                    )

            # Vérifier si le joueur a gagné
            if mot_cache == mot_secret:
                return render_template(
                    "win.html",
                    nom=nom,
                    mot_secret=mot_secret
                )

    return render_template(
        "play.html",
        nom=nom,
        mot_secret=mot_secret,
        mot_cache=mot_cache
    )


if __name__ == "__main__":
    app.run(debug=True)