import cloudinary
from flask import Flask, render_template
from flask_mysql_connector import MySQL
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, CLOUD_NAME, API_KEY, API_SECRET
from flask_login import LoginManager, login_required, current_user
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

    cloudinary.config(
       cloud_name=CLOUD_NAME,
       api_key=API_KEY,
       api_secret=API_SECRET,
       secure=True,
    )

    mysql.init_app(app)
    csrf.init_app(app)

    login.init_app(app)
    login.login_view = 'auth_bp.login'
    login.login_message = 'Please log in to access this page.'

    @app.route('/')
    def index():
        return render_template('home.html')
    
    #Blueprints
    from .controller import auth
    from .controller import main
    from .controller import post
    from .controller import user
    from .controller import profile_c
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(post.post_bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(profile_c.profile_bp)

    return app