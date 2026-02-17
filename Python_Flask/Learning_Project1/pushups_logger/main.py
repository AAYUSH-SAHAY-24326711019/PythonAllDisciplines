from flask import Blueprint, render_template,url_for
from flask_login import login_required, current_user

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

# -------------------profile page code Starts-----------------------
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)
# -------------------profile page code Ends-----------------------