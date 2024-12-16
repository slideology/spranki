from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_assets import Environment, Bundle
from config.config import config

cache = Cache()
limiter = Limiter(key_func=get_remote_address)
assets = Environment()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    cache.init_app(app)
    limiter.init_app(app)
    Talisman(app, content_security_policy=None)
    assets.init_app(app)

    # Asset bundles
    css = Bundle(
        'css/style.css',
        filters='cssmin',
        output='gen/packed.css'
    )
    js = Bundle(
        'js/main.js',
        filters='jsmin',
        output='gen/packed.js'
    )
    assets.register('css_all', css)
    assets.register('js_all', js)

    # Register blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint, url_prefix='/contact')

    return app
