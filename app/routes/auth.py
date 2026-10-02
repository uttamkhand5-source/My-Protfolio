from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/admin/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username","")).first()
        if user and check_password_hash(user.password_hash, request.form.get("password","")):
            login_user(user)
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin/login.html")

@auth_bp.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
