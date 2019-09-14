"""Model and database functions for Run Ratings project"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    # runs = db.relationship('Run')
    # db.ForeignKey('run.run_id')
    comments = db.relationship('Comments')


class Comments(db.Model):

    __tablename__ = "comments"

    comments_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)
    run_id = db.Column(db.Integer,db.ForeignKey('run.run_id'),nullable=False)
    fake_comments = db.Column(db.String(200),nullable=True)

    user = db.relationship('User')
    run = db.relationship('Run')

    def __repr__(self): 
       return f'Comments {self.comments_id}, {self.user_id}'   

class Run(db.Model):

    __tablename__ = "run"

    run_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    run_name = db.Column(db.String(200))

    comments = db.relationship('Comments')


# class All_Runs(db.Model):

#     __tablename__ = "all_runs"

#     all_runs_id = db.Column(db.String(200),nullable=True,primary_key=True)
#     user_id = db.Column(db.Integer, nullable=True)
#     run_id = db.Column(db.String(200),nullable=True)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///run_data'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    db.app = app   
    db.init_app(app)

    

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")