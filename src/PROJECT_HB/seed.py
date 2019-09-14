from model import connect_to_db, db, User, Comments, Run

def load_users():

    print("Users")

    User.query.delete()

    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, name = row.split("|")

        user = User(name=name)

        db.session.add(user)
    db.session.commit()

def load_comments():

    print("Comments")

    Comments.query.delete()

    for row in open("seed_data/u.comments"):
        row = row.rstrip()
        comment_id, fake_comments, user_id,run_id = row.split('|')

        comment = Comments(fake_comments=fake_comments,  
        user_id = user_id, run_id = run_id)
        db.session.add(comment)
    db.session.commit()

def load_runs():

    print("Runs")

    Run.query.delete()

    for row in open("seed_data/u.runs"):
        row = row.rstrip()
        run_id, run_name = row.split('|')

        runs =Run(run_name=run_name)

        db.session.add(runs)
    db.session.commit()





if __name__ == "__main__":
    from server import app

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data 
    load_users()
    load_runs()
    load_comments()

    
