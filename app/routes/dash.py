from flask import Blueprint,render_template,redirect,request,url_for,session,flash,get_flashed_messages,send_file
from app import db
from app.models import urls
import secrets
import string
import qrcode
import io
dash_bp=Blueprint("dash",__name__)

@dash_bp.route("/")
def dash():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    Urls=urls.query.filter_by(username=session["user"]).all()
    return render_template("dash.html",Urls=Urls)
ALPHABET = string.ascii_letters + string.digits

def generate_code(length=8):
    return ''.join(secrets.choice(ALPHABET) for i in range(length))
@dash_bp.route("/short_url",methods=["POST"])
def short_url():
    url=request.form.get("url")
    code=generate_code()
    unique=False
    while unique!=True:
        if urls.query.filter_by(code=code).first():
            code=generate_code()
        else:
            unique=True
    if unique==True:
        new_url=urls(url=url,code=code,username=session["user"])
        db.session.add(new_url)
        db.session.commit()
    return redirect(url_for("dash.dash"))
@dash_bp.route("/<short_code>")
def dynamic(short_code):
    if urls.query.filter_by(code=short_code):
        Url=(urls.query.filter_by(code=short_code).first()).url
        return redirect(Url)
    return redirect(url_for("dash.dash"))
@dash_bp.route("/clear")
def clear():
    urls.query.filter_by(username=session["user"]).delete()
    db.session.commit()
    return redirect(url_for("dash.dash"))
@dash_bp.route("/qr/<short_code>")
def generate_qr(short_code):
    url = "http://127.0.0.1:5000/"+short_code

    img = qrcode.make(url)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        download_name=f"{short_code}.png"
    )