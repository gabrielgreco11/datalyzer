from flask import Flask, render_template, request, url_for, redirect, session, send_file, jsonify
import json
import requests
import datetime
import os
import scrapper

application = Flask(__name__)
application.secret_key = "vS44D3LML9gi0vu1SAsjYePZ5TM6ecVyjgJcgZeMNVXS6HBkiy"


@application.route("/")
def home():
    return redirect("/timer/17:00")
    with open("config.json") as f:
        data = json.load(f)
    user_agent = request.user_agent.string
    if 'Mobile' in user_agent or 'Tablet' in user_agent:
        print("mobile")
    else:

        return render_template("home.html")


@application.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@application.route("/rick")
def rick_role():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@application.route("/timer/<date>")
def timer(date):
    return render_template("timer.html")


@application.route("/restart")
def restart():
    open("restart", "w")
    return "Erfolgreich Gestartet"


@application.route("/scrapper")
def scrapper_start():
    return scrapper.Web()


@application.route("/scrapper/show")
def scrapper_show():
    with open(f"output/{datetime.datetime.now().strftime('%d_%m')}.json") as f:
        data = json.load(f)
    return data


@application.route("/log")
def log_show():
    file_content = ""
    try:
        with open("log.txt", 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                file_content = file_content + f" {line}<br>"
    except FileNotFoundError:
        return "Die Datei wurde nicht gefunden."

    file_content.replace("\n", "<br>")
    return file_content


if __name__ == "__main__":
    """with open("config.json") as f:
        data = json.load(f)"""
    # scrapper()
    application.run(host="0.0.0.0", debug=True, port=5000)
