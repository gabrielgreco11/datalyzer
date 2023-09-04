from flask import Flask, render_template , request,url_for, redirect, session, send_file,jsonify
import json, requests, datetime
import os
def scrapper():
    print("Test")
    api_key, country_codes = setup()

    for country_code in country_codes:
        items = api_requests(country_code, api_key)
        converter(items, country_code)






def api_requests(country_code, api_key, next_page_token="&"):
    country_data = []

    while next_page_token is not None:
        request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{next_page_token}chart=mostPopular&regionCode=DE&maxResults=50&key={api_key}"
        request = requests.get(request_url)
        if request.status_code == 429:
            print("Temp-Bann")
            exit(-4)
        video_data_page = request.json()
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        
        items = video_data_page.get('items', [])
    return items


def converter(items, country):
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    with open(f"{output_dir}/{datetime.datetime.now().strftime('%d_%m')}.json") as f:
        data = json.load(f)
    data[country] = {
        datetime.datetime.now().strftime('%H'):{}
    }
    
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        if "statistics" not in video:
            continue
            
        if not "likeCount" in video['statistics']:
            video['statistics']["likeCount"] = "not found"
        if not "commentCount" in video['statistics']:
            video['statistics']["commentCount"] = "not found"

        data[country][datetime.datetime.now().strftime('%H')][video['id']] = {
            "video_title":video['snippet']["title"],
            "desciription":video['snippet']["description"],
            "publishedAt": video['snippet']["publishedAt"],
            "channel":{
                "channelTitle" : video['snippet']["channelTitle"],
                "channelId": video['snippet']["channelId"]
            },
            "meta_data": {
                "viewCount": video['statistics']["viewCount"],
                "likeCount": video['statistics']["likeCount"],
                "commentCount": video['statistics']["commentCount"],
                "thumbnail": video['snippet']["thumbnails"]["default"]["url"]

            }
        }
    with open(f"{output_dir}/{datetime.datetime.now().strftime('%d_%m')}.json", "w")as f:
        json.dump(data, f, indent=4)

       


def setup():
    api_key = "AIzaSyDQpVIFuKXKv_GKgroa_CMPP_tOuzbMmcw"
    

    with open("config.json") as f:
        country_json = json.load(f)["country"]
    country_codes = [x for x in country_json.keys()]

    return api_key, country_codes

