from flask import Flask, render_template, request, url_for, redirect, session, send_file, jsonify
import json
import requests
import datetime
import os
import scrapper

application = Flask(__name__)
application.secret_key = "vS44D3LML9gi0vu1SAsjYePZ5TM6ecVyjgJcgZeMNVXS6HBkiy"
def scrapper_formater(date):
    folder_path = "output/"
    if date == "last": 
        file_name = folder_path + datetime.datetime.now().strftime('%d_%m') + ".json"
        data = {}
        try:
            with open(file_name) as f:
                data[datetime.datetime.now().strftime('%d_%m')] = json.load(f)
            
        except FileNotFoundError:
            scrapper.Web()
            return "Heute wurde noch keine Daten gescapt. Es wurde gerade gestartet. Versuche es in 5 Minuten erneut"
    else:
        file_list = os.listdir(folder_path)
        files = [os.path.join(folder_path, file) for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
        data = {}
        for x in files:
            file_name = "".join(x.split(folder_path)[1:])
            file_name = "".join(file_name.split(".json")[0:])
            with open(x) as f:
                data[file_name] = json.load(f)
    

    finall_data = {"average":{}}

    for day in data.keys():

        ##### sort 
        sorted_likes_data = {hour: sort_channels_by_likes(data[day][hour]) for hour in data[day].keys()}
        sorted_views_data = {hour: sort_channels_by_views(data[day][hour]) for hour in data[day].keys()}
        sorted_subs_data = {hour: sort_channels_by_subs(data[day][hour]) for hour in data[day].keys()}
        
        finall_data[day] = {
            "likes": sorted_likes_data,
            "views": sorted_views_data,
            "subs": sorted_subs_data
        }


        # average day
        finall_data[day]["average_day"] = {}
        for hour in data[day].keys():
            
            for channel in data[day][hour].keys():
                try:
                    finall_data[day]["average_day"][channel]
                except KeyError:
                    finall_data[day]["average_day"][channel] = {
                        "likes": [],
                        "subs": [],
                        "views": []
                    }
                for which in data[day][hour][channel].keys():
                    if which == "url":
                        finall_data[day]["average_day"][channel]["url"] = data[day][hour][channel][which]
                    else:
                        finall_data[day]["average_day"][channel][which].append(data[day][hour][channel][which])

        keys_to_remove = []

        for channel in finall_data[day]["average_day"].keys():
            for which in finall_data[day]["average_day"][channel].keys():
                if not which == "url":
                    if finall_data[day]["average_day"][channel][which] == []:
                        keys_to_remove.append((channel, which))
                    else:
                        finall_data[day]["average_day"][channel][which] = int(sum(finall_data[day]["average_day"][channel][which]) / len(finall_data[day]["average_day"][channel][which]))
                        
                        try:
                            finall_data["average"][channel]
                        except KeyError:
                            finall_data["average"][channel] = {
                                "likes": [],
                                "subs": [],
                                "views": []
                            }
                        finall_data["average"][channel][which].append(finall_data[day]["average_day"][channel][which])
        for channel, which in keys_to_remove:
            finall_data[day]["average_day"][channel].pop(which)

    # average
    keys_to_remove = []
   
    for channel in finall_data["average"].keys():
            for which in finall_data["average"][channel].keys():
                if not which == "url":
                    if finall_data["average"][channel][which] == []:
                        keys_to_remove.append((channel, which))
                    else:
                        finall_data["average"][channel][which] = int(sum(finall_data["average"][channel][which]) / len(finall_data["average"][channel][which]))

    for channel, which in keys_to_remove:
        finall_data["average"][channel].pop(which)    

    #######  clean Numbers

    iteams_to_modify = []
    iteams_to_modify_average_day= []
    iteams_to_modify_average= []

    for day in finall_data.keys():
        if not "average" in day:
            for tags in finall_data[day].keys():
                if not "average" in tags:
                    for hours in finall_data[day][tags].keys():
                        for channel in finall_data[day][tags][str(hours)].keys():
                            for which in finall_data[day][tags][str(hours)][channel].keys():
                                if not which == "url"   :
                                    iteams_to_modify.append((day, tags, str(hours), channel, which))
                else:
                    for channel in finall_data[day][tags].keys():
                            for which in finall_data[day][tags][channel].keys():
                                if not which == "url"   :
                                    iteams_to_modify_average_day.append((day, tags, channel, which))
        else:
            for channel in finall_data[day]:
                for which in finall_data[day][channel].keys():
                    if not which == "url":
                        iteams_to_modify_average.append((day, channel, which))
    
    for day, tags, hours, channel, which in iteams_to_modify:
        finall_data[day][tags][str(hours)][channel][f"{which}_clean"] =clean_nummber(numb=finall_data[day][tags][str(hours)][channel][which])

    for day, tags, channel, which in iteams_to_modify_average_day:
        finall_data[day][tags][channel][f"{which}_clean"] =clean_nummber(numb=finall_data[day][tags][channel][which])

    for day, channel, which in iteams_to_modify_average:
        finall_data[day][channel][f"{which}_clean"] = clean_nummber(numb=finall_data[day][channel][which])



    
    return finall_data

def clean_nummber(numb):
    if len(str(numb)) > 7:
        return f"{round(numb / 10000000,1)} Mio"
    elif len(str(numb)) > 6:
        return f"{round(numb / 1000000,1)} K"

def sort_channels_by_likes(data):
    sorted_channels = sorted(data.items(), key=lambda x: x[1].get('likes', 0), reverse=True)
    return dict(sorted_channels)

def sort_channels_by_views(data):
    sorted_channels = sorted(data.items(), key=lambda x: x[1].get('views', 0), reverse=True)
    return dict(sorted_channels)

def sort_channels_by_subs(data):
    sorted_channels = sorted(data.items(), key=lambda x: x[1].get('subs', 0), reverse=True)
    return dict(sorted_channels)



@application.route("/")
def home():
    return render_template("index.html")

    

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
   return scrapper_formater("")

@application.route("/static/image/<img>")
def img(img):
    return send_file(f"images/{img}")


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=5000)
 