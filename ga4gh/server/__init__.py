from flask import Flask
from werkzeug import ImmutableDict


# haml support
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
