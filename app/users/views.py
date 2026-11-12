from flask import render_template, request, redirect, url_for, session, flash, make_response
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
    color_scheme = request.cookies.get("color_scheme", "light")
    if color_scheme not in ("light", "dark"):
        color_scheme = "light"
    return render_template(
        "profile.html",
        title="Профіль",
        username=session["username"],
        cookies=request.cookies,
        color_scheme=color_scheme,
    )


@users_bp.route("/set_color/<string:scheme>")
def set_color(scheme):
    if "username" not in session:
        flash("Для доступу до профілю потрібно увійти в систему.", "danger")
        return redirect(url_for("users.login"))

    if scheme not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("users.profile"))

    scheme_label = "темну" if scheme == "dark" else "світлу"
    flash(f"Обрано {scheme_label} кольорову схему.", "success")
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("color_scheme", scheme, max_age=30 * 24 * 60 * 60)
    return response


@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Для доступу до профілю потрібно увійти в систему.", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("cookie_key", "").strip()
    value = request.form.get("cookie_value", "").strip()
    max_age_raw = request.form.get("cookie_age", "").strip()

    if not key:
        flash("Вкажіть ключ кукі!", "danger")
        return redirect(url_for("users.profile"))

    max_age = None
    if max_age_raw:
        if not max_age_raw.isdigit() or int(max_age_raw) <= 0:
            flash("Термін дії кукі має бути додатним числом у секундах!", "danger")
            return redirect(url_for("users.profile"))
        max_age = int(max_age_raw)

    flash(f"Кукі '{key}' успішно додано!", "success")
    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)
    return response


@users_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Для доступу до профілю потрібно увійти в систему.", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("delete_key", "").strip()
    if not key:
        flash("Вкажіть ключ кукі для видалення!", "danger")
        return redirect(url_for("users.profile"))

    if key == "session":
        flash("Системну кукі 'session' не можна видалити тут. Використовуйте кнопку 'Вийти'.", "warning")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash(f"Кукі з ключем '{key}' не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    flash(f"Кукі '{key}' успішно видалено!", "success")
    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    return response


@users_bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Для доступу до профілю потрібно увійти в систему.", "danger")
        return redirect(url_for("users.login"))

    cookies_to_delete = [key for key in request.cookies if key != "session"]
    if not cookies_to_delete:
        flash("Немає користувацьких кукі для видалення.", "info")
        return redirect(url_for("users.profile"))

    flash("Усі користувацькі кукі успішно видалено!", "success")
    response = make_response(redirect(url_for("users.profile")))
    for key in cookies_to_delete:
        response.delete_cookie(key)
    return response


@users_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))
