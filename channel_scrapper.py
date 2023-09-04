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

    today = datetime.date.today()
    two_months_ago = today - datetime.timedelta(days=60)
    published_after = two_months_ago.isoformat() + 'T00:00:00Z'
    published_before = today.isoformat() + 'T00:00:00Z'
    while next_page_token is not None:
        request_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&order=rating&type=channel&regionCode={country_code}&publishedAfter={published_after}&publishedBefore={published_before}&key={api_key}'
        request = requests.get(request_url)
        if request.status_code == 429:
            print("Temp-Bann")
            exit(-4)
        video_data_page = request.json()
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        channels = []
        for item in video_data_page.get('items', []):
            if item['id']['kind'] == 'youtube#channel':
                channel_id = item['id']['channelId']
                channel_name = item['snippet']['title']
                subscriber_count = None  # Hier können Sie die Abonnentenzahl abrufen, falls gewünscht.

                channels.append({
                    'Channel Name': channel_name,
                    'Channel ID': channel_id,
                    'Subscriber Count': subscriber_count,
                })
        for channel in channels:
            print(f"Channel Name: {channel['Channel Name']}")
            print(f"Channel ID: {channel['Channel ID']}")
            print(f"Subscriber Count: {channel['Subscriber Count']}")
            print()
        with open(f"{output_dir}/{datetime.datetime.now().strftime('%d_%m')}.json", "w")as f:
            json.dump(video_data_page, f, indent=4)
    exit(-4)


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



if __name__ == "__main__":
    with open("config.json") as f:
        data = json.load(f)
    output_dir = "output/"
    scrapper()

