from flask import Flask, render_template , request,url_for, redirect, session, send_file,jsonify
import json, requests, datetime
import os

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




if __name__ == "__main__":
    """with open("config.json") as f:
        data = json.load(f)"""
    #scrapper()
    application.run(host="0.0.0.0",debug=True,port=5000)