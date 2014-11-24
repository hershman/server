from flask import Flask

# haml support
from werkzeug import ImmutableDict
class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(extensions=['jinja2.ext.autoescape',
                                              'jinja2.ext.with_',
                                              'hamlish_jinja.HamlishExtension'])

# App
app = FlaskWithHamlish(__name__)
app.config.from_object('config')
app.config["VariantBackend"] = None
app.jinja_env.hamlish_mode = "indented"

import views
