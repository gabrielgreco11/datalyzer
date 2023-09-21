from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import Flask, render_template , request,url_for, redirect, session, send_file,jsonify
import json, requests, datetime, os

def clean_numb( input_str):
    num = input_str
    
    if "." in input_str:
        # Entfernen von Tausendertrennzeichen und Nicht-Ziffern (z.B. "," und "\\xa0")
        clean_str = ''.join(filter(str.isdigit, input_str))
        # Konvertierung in Ganzzahl
        num = int(clean_str)
        num *= 1000

    if "Mio" in input_str:
        # Entfernen von Nicht-Ziffern (z.B. "," und "\\xa0")
        clean_str = ''.join(filter(str.isdigit, input_str))
        # Konvertierung in Ganzzahl
        num = int(clean_str)
        num *= 1000000

    return num

def Web():
    try:
        # Webdriver-Optionen konfigurieren, um den Browser unsichtbar zu machen
        chrome_options = Options()
        chrome_options.headless = True

        # Pfad zum Chromedriver angeben (stellen Sie sicher, dass Sie den Chromedriver heruntergeladen haben)
        chromedriver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

        # URL der Website
        URL_list = ["https://nindo.de/charts/youtube/views", "https://nindo.de/charts/youtube/likes","https://nindo.de/charts/youtube/followers"]
        views = {} # a list to store quotes
        likes= {}
        subs = {}
        # Selenium-Webdriver initialisieren
        versuch = 0
        while len(URL_list) > 0:
            versuch = versuch + 1
            for URL in URL_list:
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(URL)
                driver.implicitly_wait(30 * versuch)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                driver.quit()
                

                table = soup.find('div', attrs = {'class':'mx-auto max-w-screen-md'})


                for row in table.findAll('a'):
                    if "https://nindo.de/charts/youtube/views" ==  URL:
                        views[row.findAll('span')[2].text] = {
                            'url': row['href'],
                            'views': row.div.span.text
                        }
                    elif "https://nindo.de/charts/youtube/likes" == URL:            
                        likes[row.findAll('span')[2].text] = {
                            'url': row['href'],
                            'likes': row.div.span.text
                        }
                    elif "https://nindo.de/charts/youtube/followers" == URL:
                        subs[row.findAll('span')[2].text] = {
                            'url': row['href'],
                            'subs': row.div.span.text
                        }
            if len(views.keys()) > 2 and  "https://nindo.de/charts/youtube/views" in URL_list :
                URL_list.remove("https://nindo.de/charts/youtube/views")
            
            if len(likes.keys()) > 2 and "https://nindo.de/charts/youtube/likes" in URL_list:
                URL_list.remove("https://nindo.de/charts/youtube/likes")
            
            if len(subs.keys()) > 2 and "https://nindo.de/charts/youtube/followers" in URL_list:
                URL_list.remove("https://nindo.de/charts/youtube/followers")
            print(URL_list)
                    

        # Jetzt enthält das 'quotes'-Dictionary die gewünschten Daten
        final = {}
        for x in views.keys():
            if x == "":
               continue
            else:
                final[x] = {
                    "url": views[x]["url"]
                }
                final[x]["views"] = clean_numb(views[x]["views"])
                if x in subs.keys():
                    final[x]["subs"]= clean_numb(subs[x]["subs"])
                if x in likes.keys():
                    final[x]["likes"]= clean_numb(likes[x]["likes"])
        for x in subs.keys():
            if not x in final.keys():
                final[x] = {
                "url": subs[x]["url"]
            }
            final[x]["subs"] = clean_numb(subs[x]["subs"])
            if x in likes.keys():
                final[x]["likes"]= clean_numb(likes[x]["likes"])

        for x in likes.keys():
            if not x in final.keys():
                final[x] = {
                "url": likes[x]["url"]
            }
            final[x]["likes"] = clean_numb(likes[x]["likes"])


        output_dir = "output/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        try:
            with open(f"{output_dir}/{datetime.datetime.now().strftime('%d_%m')}.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("New File")
            data = {}    

        data[datetime.datetime.now().strftime('%H')] = final

        with open(f"{output_dir}/{datetime.datetime.now().strftime('%d_%m')}.json", "w") as f:
                json.dump(data, f, indent=4)
        return "Erfolgreich"
    except Exception as e:
        return f"ERROR: {str(e)}"




########################################################################################################################################################################################################



def chartscrapper( ):
    try:
        api_key, country_codes =  setup()

        for country_code in country_codes:
            items =  api_requests(country_code, api_key)
            converter(items, country_code)
    except Exception as e:
        return f"ERROR: {str(e)}"





def api_requests( country_code, api_key, next_page_token="&"):
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


def converter( items, country):
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

    


def setup( ):
    api_key = "AIzaSyDQpVIFuKXKv_GKgroa_CMPP_tOuzbMmcw"
    

    with open("config.json") as f:
       country_json = json.load(f)["country"]
    country_codes = [x for x in country_json.keys()]

    return api_key, country_codes

