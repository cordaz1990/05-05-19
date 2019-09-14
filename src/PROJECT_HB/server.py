"""Run Ratings."""
from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Comments, Run


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/') 
def index():
    """Homepage."""
    # create two links, one for homepage and another for view comments
    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def register_form():
    
    return render_template("register_form.html")    

@app.route('/register', methods=['POST'])
def register_process():

    print('this is what the form looks like:')
    print(request.form)

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]

    new_user = User(name=firstname + ' ' + lastname)
    db.session.add(new_user)
    db.session.commit()
    session['user'] = new_user.user_id
    
    return redirect("/")

@app.route('/log_in', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/log_in', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    name = request.form["name"]
    lastname = request.form["lastname"]
    email = request.form["email"]

    

    user = User.query.filter_by(name=name).first()

    # check to make sure that user is in the DB and exsists
    # if the users isnt in the DB, redirect to SIGNUP page

    # check to make sure that users password is the same as what they put
    # if its ok, then set the session, otherwise show an error

    session["user"] = user.user_id

    
    return redirect("/add_run_comment")

 

@app.route('/add_run_comment', methods=["GET", "POST"])

def add_run_comment():
    user = session['user'] 
    # check to make sure there is a user, otherwise direct to LOGIN

    if request.method == 'POST':
        # get the data from the subbmited form 
        print(request.form)
        comment = request.form['comment']
        runid = request.form['run']

        # save to db
        new_comment = Comments(user_id=user, fake_comments=comment, run_id=runid)
        db.session.add(new_comment)
        db.session.commit()
        all_comments = Comments.query.options(db.joinedload('user'),db.joinedload('run')).all()
        return render_template("table_of_runs.html",comments=all_comments)

    else: 
        all_runs = Run.query.all()
        user = User.query.filter_by(user_id=user).first()
        return render_template("add_run_comment.html", runs=all_runs, user_name=user.name)


@app.route('/view_runs')
def view_runs():
    all_comments = Comments.query.options(db.joinedload('user'),db.joinedload('run')).all()
    return render_template("table_of_runs.html",comments=all_comments)

@app.route('/users/<user_id>')
def user_detail(user_id):
    
    user = User.query.get(user_id)

    return render_template("run_detail.html", user=user)
    



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app) 



    app.run(port=5000, host='0.0.0.0')