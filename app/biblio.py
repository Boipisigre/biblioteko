from flask import render_template, redirect, request, session, url_for, flash
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
	return render_template('livres.html', posts=lesnotes)

@app.route("/ajout")
def addlivre():
	return render_template('index.html')

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
    trouvé=False
    if len(lesnotes) > 0:
        trouvé=True

    if not(trouvé):
        flash('Livre non trouvé!')

    return render_template('livres.html', posts=lesnotes)

@app.route("/recheruser")
def recheruser():
    # return "résultat de ma recherche"
    txt_recherche =request.args.get("user")
    # notepage = render_template("notes.html")
    lesnotes=get_notes_user(txt_recherche)
    trouvé=False
    if len(lesnotes) > 0:
        trouvé=True

    if not(trouvé):
        flash('Livre non trouvé!')

    return render_template('livres.html', posts=lesnotes)

@app.route("/connection")
def login():
	return render_template('index.html')

@app.route("/deconnection")
def logout():
	return render_template('index.html')

@app.route("/enregistre")
def register():
	return render_template('index.html')
