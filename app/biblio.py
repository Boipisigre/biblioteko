from flask import render_template, redirect, request, session, url_for, flash
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import EmailForm
from flask_babel import Babel
from app import app, babel
from database import *

def get_locale():
	# If the user has set up the language manually it will be stored in the session
	try:
		language = session['language']
	except KeyError:
		language = None
	if language is not None:
		return language
	return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_conf_var():
	return dict(
		AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
		CURRENT_LANGUAGE=session.get(
			'language',
			request.accept_languages.best_match(app.config['LANGUAGES'].keys())
		)
	)

# This route handles the language change and will store the selected language in the session
@app.route('/language/<language>')
def set_language(language=None):
	session['language'] = language
	return redirect(url_for('homepage'))

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/livres")
def livres():
	lesnotes=get_notes("*")
	return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route('/<int:post_id>/')
def post(post_id):
	post = get_post(post_id)
	rows=[]
	for ligne in post:
		ligne = dict(ligne)
		print(ligne)
		rows.append(ligne)

		return render_template('unlivre.html', post=rows[0])

@app.route("/ajout")
def addlivre():
	return render_template('ajoutlivre.html')

@app.route("/ajoutnote", methods=('GET', 'POST'))
def ajoutlivre():
	if request.method == 'POST':
		txt_titre = request.form['titre']
		txt_id = request.form['id']
		txt_rubrique = request.form['rubrique']
		txt_auteur = request.form['auteur']
		txt_editeur = request.form["editeur"]
		add_notes(txt_id, txt_titre,txt_rubrique,txt_auteur, txt_editeur)
	return livres()


@app.route("/cherparuser")
def cherparuser():
	return render_template('recherche.html', query="user")

@app.route("/cherpartitre")
def cherpartitre():
	return render_template("recherche.html",query="titre")

@app.route("/rechercher")
def rechercher():
    # return "résultat de ma recherche"
    txt_recherche =request.args.get("titre")
    lesnotes=get_notes(txt_recherche)
    return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route("/recheruser")
def recheruser():
    # return "résultat de ma recherche"
    txt_recherche =request.args.get("user")
    # notepage = render_template("notes.html")
    lesnotes=get_notes_user(txt_recherche)
    return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route("/connection")
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST',"GET"])
def do_admin_login():
    nom=request.args.get("username")
    pwd=get_user(nom)
    session['logged_in'] = False
    if pwd is None :
        flash('Utilisateur inconnu!')
    else:
        if check_password_hash(pwd[0], request.args.get("password")):
            session['logged_in'] = True
            session['user_name'] = nom
        else:
            flash('Mot de passe éroné!')

    return render_template("index.html")

@app.route('/register', methods=['POST',"GET"])
@app.route("/enregistre", methods=['POST',"GET"])
def register():
    return render_template("register.html")

@app.route('/logout')
@app.route("/deconnection")
def logout():
    session['logged_in'] = False
    return render_template("index.html")


@app.route('/registeruser', methods=['POST',"GET"])
def registeruser():

    nom=request.args.get("username")
    pwd=request.args.get("password")
    hashpwd=generate_password_hash(pwd)
    add_user(nom, hashpwd)
    session['logged_in'] = False
    return render_template("index.html")

@app.route('/redakti/<int:id>', methods=('GET', 'POST'))
def redakti(id):
	post = get_post(id)
	if request.method == 'POST':
		autoro = request.form['Autoro']
		titolo = request.form['titolo']
		enhavo = request.form['enhavo']
		if not titolo:
			flash('Un titre est obligatoire!')
		else:
			update_note(autoro, titolo, enhavo, id)

			return livres()

	return render_template('editer.html', post=post[0])

@app.route('/<int:id>/forigi', methods=('POST',))
def delete(id):
    post = get_post(id)
    delete_note(id)
    flash('La note "{}" a été supprimée!'.format(post[0]['titre']))

    return notes()
