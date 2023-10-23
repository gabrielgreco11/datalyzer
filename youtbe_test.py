import os
from googleapiclient.discovery import build




def get_youtber_date(channel_url):
    API_KEY = 'AIzaSyDQpVIFuKXKv_GKgroa_CMPP_tOuzbMmcw'
    channel_url.replace("/","").replace("-","")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    response = youtube.channels().list(
        part="id",
        forUsername=channel_url
    ).execute()

    if 'items' in response:
        channel_id = response['items'][0]['id']
        channel_response = youtube.channels().list(
                part='snippet',
                id=channel_id
            ).execute()

        if 'items' in channel_response:
            print(channel_response['items'][0]["snippet"]["thumbnails"]["high"]["url"])
            channel_info = channel_response['items'][0]['snippet']
            channel_description = channel_info['description']
            print(channel_description)

        
        
    else:
        print("Channel-ID konnte nicht gefunden werden.")

# import os
# import google_auth_oauthlib.flow
# from googleapiclient.discovery import build

# # API-Zugriffsinformationen
# api_key = 'AIzaSyDQpVIFuKXKv_GKgroa_CMPP_tOuzbMmcw';  # Ersetze 'DEIN_API_KEY' durch dein eigenes YouTube Data API Key

# # Initialisiere die YouTube Data API
# youtube = build('youtube', 'v3', developerKey=api_key)

# def get_channel_description(channel_name):
#     try:
#         # Gib hier die Kanal-ID des YouTube-Kanals ein
#         channel_id = channel_name  # Ersetze 'channel_name' durch die Kanal-ID oder den Benutzernamen
        
#         # Rufe Kanal-Details ab
#         channel_response = youtube.channels().list(
#             part='snippet',
#             id=channel_id
#         ).execute()

#         if 'items' in channel_response:
#             channel_info = channel_response['items'][0]['snippet']
#             channel_description = channel_info['description']
#             return channel_description

#     except Exception as e:
#         print(f"Fehler beim Abrufen der Kanalbeschreibung: {str(e)}")
    
#     return None

# if __name__ == '__main__':
#     # Gib hier die Kanal-ID oder den Benutzernamen des YouTube-Kanals ein, dessen Beschreibung du abrufen möchtest.
#     channel_name = 'UCTXeJ33DzXI2veQpKfrvaYw'  # Ersetze 'julien-bam' durch die Kanal-ID oder den gewünschten Benutzernamen
    
#     channel_description = get_channel_description(channel_name)
#     if channel_description:
#         print(f"Beschreibung des Kanals ({channel_name}): {channel_description}")
#     else:
#         print("Kanalbeschreibung konnte nicht abgerufen werden.")
