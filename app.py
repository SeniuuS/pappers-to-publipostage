from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    from routes import main
    app.register_blueprint(main.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)