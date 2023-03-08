class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'v/V\x01a\x13J\x16\xf2>\x9f\xf4\x11T\xb9A'

	# Here you can list all the languages ​​that you want to use in your application
	# 'en': 'English',
	LANGUAGES = {
		'eo': 'Esperanto',
		'fr': 'Français'
	}

class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = False

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
