from flask import Flask, render_template
from flask_mysql_connector import MySQL
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect


mysql = MySQL()
login = LoginManager()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST
    )

    mysql.init_app(app)
    csrf.init_app(app)

    login.init_app(app)
    login.login_view = 'auth_bp.login'
    login.login_message = 'Please log in to access this page.'

    @app.route('/')
    def index():
        return render_template('home.html')
    
    @app.route('/loggedin')
    @login_required
    def loggedin():
        return render_template('loggedin.html')
    
    #Blueprints
    from .controller import auth
    app.register_blueprint(auth.auth_bp)

    return app