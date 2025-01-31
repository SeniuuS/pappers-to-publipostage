from flask import Flask
import os

from flask_htpasswd import HtPasswdAuth

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = Config.SESSION_SECRET_KEY
    app.config['FLASK_HTPASSWD_PATH'] = os.path.join('.htpasswd')
    app.config['FLASK_AUTH_ALL'] = True

    htpasswd = HtPasswdAuth(app)

    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    from routes import main
    app.register_blueprint(main.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=8686)
else:
    gunicorn_app = create_app()