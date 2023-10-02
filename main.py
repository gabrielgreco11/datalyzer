from flask import Flask, render_template, request, url_for, redirect, session, send_file, jsonify
import json
import requests
import datetime
import os
import scrapper

application = Flask(__name__)
application.secret_key = "vS44D3LML9gi0vu1SAsjYePZ5TM6ecVyjgJcgZeMNVXS6HBkiy"


"""@application.route("/")
def home():
    return redirect("/timer/17:00")
    with open("config.json") as f:
        data = json.load(f)
    user_agent = request.user_agent.string
    if 'Mobile' in user_agent or 'Tablet' in user_agent:
        print("mobile")
    else:

        return render_template("home.html")"""
@application.route("/")
def home():
    folder_path = "output/"
    file_list = os.listdir(folder_path)
    files = [os.path.join(folder_path, file) for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
    data = {}
    for x in files:
        file_name = "".join(x.split(folder_path)[1:])
        file_name = "".join(file_name.split(".json")[0:])
        with open(x) as f:
            data[file_name] = json.load(f)
    return data
    #### Sort nach Views ###
    view_list = []
    views = {}
    for days in data.keys():
        for hours in data[days].keys():
            for user in data[days][hours].keys():
                try:
                    view_list.append(user["views"])
                except KeyError:
                    continue
    view_list.sort()
    
"""for x in view_list:
        for days in data.keys():
            for hours in days.keys():
                for user in hours.keys():
                    try:
                        if x == user["views"]
                            print("EXIT")
                    except KeyError:
                        continue"""
    

@application.route("/base")
def base_test():
    return render_template("base.html")
@application.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@application.route("/rick")
def rick_role():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@application.route("/git")
def github():
    return redirect("https://github.com/gabrielgreco11/datalyzer")

@application.route("/rede")
def easteregg():
    return redirect("https://www.youtube.com/watch?v=FJ3N_2r6R-o")


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


if __name__ == "__main__":
    """with open("config.json") as f:
        data = json.load(f)"""
    # scrapper()
    application.run(host="0.0.0.0", debug=True, port=5000)
