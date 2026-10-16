from flask import request, redirect, url_for, render_template, abort
from app import app


@app.route("/")
def main():
    return redirect(url_for("home"))


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", title="Головна", agent=agent)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти")
