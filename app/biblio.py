from flask import render_template, redirect, request, session, url_for
from app.forms import EmailForm
from flask_babel import Babel
from app import app, babel

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
	return render_template('index.html')

@app.route("/ajout")
def addlivre():
	return render_template('index.html')

@app.route("/cherparuser")
def cherparuser():
	return render_template('index.html')

@app.route("/cherpartitre")
def cherpartitre():
	return render_template('index.html')

@app.route("/connection")
def login():
	return render_template('index.html')

@app.route("/deconnection")
def logout():
	return render_template('index.html')

@app.route("/enregistre")
def register():
	return render_template('index.html')
