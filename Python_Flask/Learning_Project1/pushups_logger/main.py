from . import db
from .models import User
from .models import Workout
from flask import Blueprint, flash, jsonify, render_template,url_for,request,redirect
from flask_login import login_required, current_user
from sqlalchemy import asc

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

# -------------------profile page code Starts-----------------------
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)

# -----------------------code to see workouts / ui start --------------------

@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')

@main.route('/new',methods=['POST'])
@login_required
def new_workout_post():
    pushups=request.form.get('pushups')
    comment=request.form.get('comment')

    # add to the database
    workout = Workout(pushups=pushups, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()
    flash('Your workout has been added')
    return redirect(url_for('main.user_workouts'))
# -----------------------code to see workouts / ui end --------------------

#---------see all the workouts start-----------------
@main.route('/all')
@login_required
def user_workouts():
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = Workout.query.filter_by(author=user).paginate(page=page,per_page =31)
    return render_template('all_workouts.html',workouts=workouts, user=user)

#---------see all the workouts end-----------------

# --------------make the updates start --------------------------
@main.route('/workout/<int:workout_id>/update', methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash('Your workout has been updated ...')
        return redirect(url_for('main.user_workouts'))


    return render_template('update_workout.html',workout=workout)

# --------------make the updates end --------------------------
# --------------delete the record start --------------------------
@main.route('/workout/<int:workout_id>/delete', methods=['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Your workout has been deleted ...')
    return redirect(url_for('main.user_workouts'))


# --------------delete the record end --------------------------

# -------------------profile page code Ends-----------------------

#------------Graphs of the pushups start---------------------
@main.route("/workoutChart")
@login_required
def workout_data():
    workouts = Workout.query \
        .filter_by(author=current_user) \
        .order_by(asc(Workout.date_posted)) \
        .all()

    data = [
        {
            "date": w.date_posted.strftime("%Y-%m-%d"),
            "pushups": w.pushups
        }
        for w in workouts
    ]

    return jsonify(data)
#------------Graphs of the pushups end---------------------