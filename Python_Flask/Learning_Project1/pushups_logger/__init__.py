from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    #code for the sql alchemy
    app.config['SECRET_KEY']='secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

    db.init_app(app)

    # ----------------code of login manager start------------------------
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    # ----------------code of login manager end------------------------

    # ----------------------code of user loader start----------------------
    from .models import User   
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        

    # ----------------------code of user loader end----------------------



    with app.app_context():
        db.create_all()      


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app