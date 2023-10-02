from flask import Flask, render_template, request, url_for, redirect, session, send_file, jsonify
import json
import requests
import datetime
import os
import scrapper

application = Flask(__name__)
application.secret_key = "vS44D3LML9gi0vu1SAsjYePZ5TM6ecVyjgJcgZeMNVXS6HBkiy"

def scrapper_formater():
    folder_path = "output/"
    file_list = os.listdir(folder_path)
    files = [os.path.join(folder_path, file) for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
    data = {}
    for x in files:
        file_name = "".join(x.split(folder_path)[1:])
        file_name = "".join(file_name.split(".json")[0:])
        with open(x) as f:
            data[file_name] = json.load(f)

    categorys = {}
    for category in ["views","likes","subs"]:
        categorys[category] ={"list":[]}
        for days in data.keys():
            for hours in data[days].keys():
                for user in data[days][hours].keys():
                    try:
                        categorys[category]["list"].append(data[days][hours][user][category])
                    except KeyError:
                        continue
        categorys[category]["list"].sort(reverse=True)
        for x in categorys[category]["list"]:
            for days in data.keys():
                for hours in data[days].keys():
                    for user in data[days][hours].keys():
                        try:
                            if x == data[days][hours][user][category]:
                                categorys[category][str(categorys[category]["list"].index(x) + 1)] = data[days][hours][user]
                        except KeyError:
                            continue
                        except ValueError:
                            continue
    return categorys

@application.route("/")
def home():
    
    data= scrapper_formater()
    return render_template("chart_frontpage.html")

    

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


@application.route("/scraper")
def scrapper_start():
    return scrapper.Web()


@application.route("/scraper/show")
def scrapper_show():
   return scrapper_formater()


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=5000)
