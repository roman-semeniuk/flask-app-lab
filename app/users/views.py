from flask import render_template, request, redirect, url_for, session, flash
from . import users_bp

USERS = {
    "user1": "12345",
    "admin": "admin",
}


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="administrator", age=45))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))
        flash("Невірне ім'я користувача або пароль! Спробуйте ще раз.", "danger")
        return redirect(url_for("users.login"))
    return render_template("login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Для доступу до профілю потрібно увійти в систему.", "danger")
        return redirect(url_for("users.login"))
    return render_template("profile.html", title="Профіль", username=session["username"])


@users_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))
