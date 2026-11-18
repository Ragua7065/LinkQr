from app import db

class login_details(db.Model):
    username=db.Column(db.String(10),nullable=False,primary_key=True)
    password=db.Column(db.String(20),nullable=False)

class urls(db.Model):
    code=db.Column(db.String(20),nullable=False,primary_key=True)
    url=db.Column(db.String(1000),nullable=False)
    username=db.Column(db.String(20),nullable=False)