from flask import Blueprint,render_template,redirect,request,url_for,session,flash,get_flashed_messages
from app import db
from app.models import login_details
auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=login_details.query.filter_by(username=username).first()
        if user and user.password==password:
            session["user"]=username
            flash("Login Success","success")
            return redirect(url_for("dash.dash"))
        else:
            flash("username or password is incorrect","fail")
    return render_template("login.html")
@auth_bp.route("/logout")
def logout():
    if "user" in session:
        session.pop("user",None)
    return redirect(url_for("auth.login"))
@auth_bp.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        username=request.form.get("rusername")
        password=request.form.get("rpassword")
        confirm_password=request.form.get("rconfirmpassword")
        if not login_details.query.filter_by(username=username).first():
            if password==confirm_password:
                new_user=login_details(username=username,password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration Sucessful","success")
                redirect(url_for("auth.login"))
            else:
                flash("username or password is incorrect","fail")
        else:
            flash("Username already exist","fail")
    return render_template("register.html")