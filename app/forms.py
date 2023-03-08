from flask_wtf import FlaskForm
from wtforms import StringField
from flask_babel import lazy_gettext

class EmailForm(FlaskForm):
	email = StringField(lazy_gettext('E-mail address'))