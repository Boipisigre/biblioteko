from flask import render_template, redirect, request, session, url_for, flash
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import EmailForm
from flask_babel import Babel, lazy_gettext
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
	message = ""
	return render_template('index.html', message=message)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/livres")
def livres():
	lesnotes=get_notes("*")
	session['reserver'] = False
	session['rendre'] = False
	return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route("/livresdispo")
def livresdispo():
	lesnotes=get_livres("*")
	session['reserver'] = True
	session['rendre'] = False
	return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

# livrespret
@app.route("/livrespret")
def livrespret():
	lesnotes=get_livresprete("*")
	session['reserver'] = False
	session['rendre'] = True
	return render_template('prete.html', posts=lesnotes, nombre=len(lesnotes))

@app.route('/<int:post_id>/')
def post(post_id):
	post = get_post(post_id)
	rows=[]
	for ligne in post:
		ligne = dict(ligne)
		# print(ligne)
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
	txt_recherche =request.args.get("titre")
	session['reserver'] = False
	session['rendre'] = False
	lesnotes=get_notes(txt_recherche)

	return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route("/recheruser")
def recheruser():
	txt_recherche =request.args.get("user")
	session['reserver'] = False
	session['rendre'] = False
	lesnotes=get_notes_user(txt_recherche)

	return render_template('livres.html', posts=lesnotes, nombre=len(lesnotes))

@app.route("/connection")
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST',"GET"])
def do_admin_login():

	message = ""
	nom=request.args.get("username")
	pwd=get_user(nom)
	session['logged_in'] = False
	if pwd is None: message=lazy_gettext('Utilisateur inconnu!')
	else:
		if check_password_hash(pwd[0], request.args.get("password")):
			session['logged_in'] = True
			session['user_name'] = nom
			session['admin'] = False
			admin=is_admin(nom)
			# print(admin[0])
			if admin[0] == 1:
				session['admin'] = True
		else:
			message=lazy_gettext('Mot de passe éroné!')

	return render_template("index.html", message=message)

@app.route('/changepwd', methods=['POST','GET'])
def changepwd():
	return render_template("chgpwd.html")

@app.route('/mdp', methods=['POST',"GET"])
def do_admin_mdp():

	message = ""

	oldpwd = request.args.get("password")
	newpwd = request.args.get("newpassword")
	hashpwd=generate_password_hash(newpwd)

	if oldpwd != newpwd :
		upd_user(session['user_name'],hashpwd)
		message = "Modification du mot de passe prise en compte"
		session['logged_in'] = False
		session['admin']=False
	else:
		message = "Nouveau mot de passe identique à l'ancien"

	return render_template("index.html", message=message)

@app.route('/register', methods=['POST',"GET"])
@app.route("/enregistre", methods=['POST',"GET"])
def register():
    return render_template("register.html")

@app.route('/logout')
@app.route("/deconnection")
def logout():
	session['logged_in'] = False
	session['admin'] = False
	return render_template("index.html")

@app.route('/user')
def user():
	lesusers=list_users()

	return render_template('users.html', posts=lesusers, nombre=len(lesusers))

@app.route('/forigi/<int:id>/', methods=('POST',''))
def forigi_konton(id):
	forigi_user(id)
	lesusers=list_users()

	return render_template('users.html', posts=lesusers, nombre=len(lesusers))

@app.route('/registeruser', methods=['POST',"GET"])
def registeruser():
	message = ' '
	code=request.args.get("code")
	if code=="Esperanto-2023" :
		nom=request.args.get("username")
		pwd=request.args.get("password")
		hashpwd=generate_password_hash(pwd)
		user=get_user(nom)
		if user :
			message=lazy_gettext('Utilisateur déjà éxistant')
		else:
			add_user(nom, hashpwd)
			message=lazy_gettext('Création Utilisateur OK')
	else:
		message=lazy_gettext('Veuillez saisir le code')

	session['logged_in'] = False
	return render_template("index.html", message=message)

@app.route('/redakti/<int:id>', methods=('GET', 'POST'))
def redakti(id):
	post = get_post(id)
	if request.method == 'POST':
		autoro = request.form['Autoro']
		titolo = request.form['titolo']
		enhavo = request.form['enhavo']
		update_note(autoro, titolo, enhavo, id)
		return livres()

	return render_template('editer.html', post=post[0])

@app.route('/forigi/<int:id>', methods=('POST',''))
def delete(id):
    post = get_post(id)
    delete_livre(id)
    flash('Le livre"{}" a été supprimée!'.format(post[0]['Titolo']))

    return livres()

@app.route('/rezervu/<int:id>')
def reservu(id):
	post = get_post(id)
	rezervu_libro(id,session['user_name'])
	flash('Le livre "{}" a été réservé!'.format(post[0]['Titolo']))
	return livres()

@app.route('/redonu/<int:id>')
def redonu(id):
	print (id)
	post = get_post(id)
	redonu_libro(id)
	flash('Le livre "{}" a été rendu!'.format(post[0]['Titolo']))
	return livres()
