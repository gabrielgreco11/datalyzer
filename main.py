from flask import Flask, render_template, request, url_for, redirect, session, send_file, jsonify
import json
import requests
import datetime
import os
from googleapiclient.discovery import build
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
    finall_data = {
        "average":{}
        }

    for day in data.keys():
        finall_data[day] ={
            "average_day":{},
            "scoreboard":{
                "likes": {},
                "subs": {},
                "views": {}
                }
        }
        for hour in data[day].keys():
            for channel in data[day][hour].keys():
                if channel == "":
                    display_channel = data[day][hour][channel]["url"].replace("/","").replace("-"," ")
                else:
                    display_channel = channel
                try:
                    finall_data[day]["average_day"][display_channel]
                except KeyError:
                    finall_data[day]["average_day"][display_channel] = {
                        "likes": [],
                        "subs": [],
                        "views": []
                    }
                for which in data[day][hour][channel].keys():
                    if which == "url":
                        finall_data[day]["average_day"][display_channel]["url"] = data[day][hour][channel][which]
                    else:
                        finall_data[day]["average_day"][display_channel][which].append(data[day][hour][channel][which])
        keys_to_remove = []
        items_to_modify = []
        for channel in finall_data[day]["average_day"].keys():
            for which in finall_data[day]["average_day"][channel].keys():
                if not which == "url":
                    if finall_data[day]["average_day"][channel][which] == []:
                        keys_to_remove.append((channel, which))
                    else:
                        try:
                            zahl = (sum(finall_data[day]["average_day"][channel][which]) / len(finall_data[day]["average_day"][channel][which]))
                            zahl = int(zahl)
                            finall_data[day]["average_day"][channel][which] = zahl
                            items_to_modify.append((channel,which,zahl))
                            try:
                                finall_data["average"][channel]
                            except KeyError:
                                finall_data["average"][channel] = {
                                    "likes": [],
                                    "subs": [],
                                    "views": []
                                }
                            finall_data["average"][channel][which].append(finall_data[day]["average_day"][channel][which])
                        except TypeError:
                            continue
                else:
                    finall_data["average"][channel]["url"] = finall_data[day]["average_day"][channel][which]
        for channel, which in keys_to_remove:
            try:
                finall_data[day]["average_day"][channel].pop(which)
            except KeyError:
                continue

        channels = []
        for channel_name, channel_data in finall_data[day]["average_day"].items(): 
            channel_info = {
            "channel_name": channel_name,
            "url":channel_data.get("url", ""),
            "subs": channel_data.get("subs", 0),
            "views": channel_data.get("views", 0),
            "likes": channel_data.get("likes", 0),
            }
            channels.append(channel_info)
        sorted_channels_subs = sorted(channels, key=lambda x: x["subs"], reverse=True)
        sorted_channels_views = sorted(channels, key=lambda x: x["views"], reverse=True)
        sorted_channels_likes = sorted(channels, key=lambda x: x["likes"], reverse=True)
        for x in [sorted_channels_subs, sorted_channels_views, sorted_channels_likes]:
            if x == sorted_channels_subs:
                z = "subs"
            elif x == sorted_channels_views:
                z = "views"
            else:
                z = "likes"
            for i, channel in enumerate(x, start=1):
                i = f"{i}."
                if not channel[z] == 0:
                    finall_data[day]["scoreboard"][z][i] = {
                        "name":channel['channel_name'],
                        "url":channel['url']
                    }
                    if 'subs' in channel:
                        if not channel['subs'] == 0:
                            finall_data[day]["scoreboard"][z][i]["subs"]= clean_nummber(channel['subs'])
                    if 'views' in channel:
                        if not channel['views'] == 0:
                            finall_data[day]["scoreboard"][z][i]["views"]= clean_nummber(channel['views'])
                    if 'likes' in channel:
                        if not channel['likes'] == 0:
                            finall_data[day]["scoreboard"][z][i]["likes"]= clean_nummber(channel['likes'])
        for channel,which,zahl in items_to_modify:
            finall_data[day]["average_day"][channel][f"{which}_clean"] = clean_nummber(zahl)
    return finall_data
    
def clean_nummber(numb):
    if len(str(numb)) > 7:
        return f"{round(numb / 10000000,1)} Mio"
    elif len(str(numb)) > 6:
        return f"{round(numb / 1000000,1)} K"
    else:
        return f"{numb}"

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
def redirect_home():
    data = scrapper_formater()
    return redirect(f"/{list(data.keys())[-1]}")

@application.route("/<date>")
def home(date):
    data = scrapper_formater()
    if not date in data.keys():
        return redirect("/")
    return render_template("index.html", data = data, date = str(date))

@application.route("/yotuber/<youtuber>")
def youtuber(youtuber):
    data = scrapper_formater()
    channel_list = []
    for channel in data["average"].keys():
        for item in data["average"][channel].keys():
            if item == "url":
                if "/"+youtuber == data["average"][channel]["url"]:
                    channel_list.append(channel)
    youtuber_display = youtuber.replace("/","").replace("-"," ").title()
    with open("pictures_data.json") as f:
        pictures_data = json.load(f)
    return render_template("fokus_one_youtuber.html",last_date=list(data.keys())[-1], youtuber_display = youtuber_display, data = data, channel_list=channel_list, channel_list_range = range(0,len(channel_list)),pictures_data = pictures_data)

@application.route("/site")
def site_without_sort():
    return redirect("/site/likes")
@application.route("/site/<sort>")
def site(sort):
    if sort in ["likes","views","subs"]:
        data=scrapper_formater()
        return render_template("sites.html", data=data, sort=sort,last_date=list(data.keys())[-1] )
    else:
        return redirect("/site")

@application.route("/template/<html>")
def render_test(html):
    return render_template(f"{html}.html")

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

@application.route("/static/image/<img>")
def img(img):
    return send_file(f"images/{img}")

@application.route("/settings")
def settings():
    with open("config.json") as f:
        data = json.load(f)
    return render_template("settings.html",data = data)

@application.route("/api/<what>/<format>")
def api(what,format):
    with open("config.json") as f:
        data = json.load(f)
    if what in data.keys():
        if data[what]["type"] == "IMG":
            return redirect(data[what]["value"])
        else:
            daten = data[what]["value"]
    if format in ["json","text"]:
        if format == "text":
            return daten
        else:
            return jsonify({what:daten})

@application.route("/api/<cmd>/<what>/<value>")
def api_edit(what, cmd, value):
    if cmd == "set":
        with open("config.json") as f:
            data = json.load(f)
        if what in data.keys():
            data[what]["value"] = value.replace("&","/")
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
    return "Erfolgreich"

@application.route("/api/get_all_data")
def api_get_data():
    return jsonify(scrapper_formater())

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=5000)
 