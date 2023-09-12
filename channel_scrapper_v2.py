from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'AIzaSyDQpVIFuKXKv_GKgroa_CMPP_tOuzbMmcw'
# Replace 'YOUR_REGION_CODE' with the 2-letter ISO 3166-1 country code (e.g., 'US' for the United States)
REGION_CODE = 'US'

def get_top_10_channels(region_code):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get the most popular videos in the specified region
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=10
    )

    response = request.execute()

    top_10_channels = []
    for item in response.get('items', []):
        video_id = item['id']
        video_title = item['snippet']['title']

        # Get the channel information for the video
        channel_request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        channel_response = channel_request.execute()

        channel_title = channel_response['items'][0]['snippet']['channelTitle']
        channel_id = channel_response['items'][0]['snippet']['channelId']

        # Get channel statistics to get the total number of subscribers
        channel_stats = youtube.channels().list(
            part='statistics',
            id=channel_id
        ).execute()

        total_subscribers = channel_stats['items'][0]['statistics']['subscriberCount']

        # Generate the link to the channel
        channel_link = f"https://www.youtube.com/channel/{channel_id}"

        top_10_channels.append((channel_title, video_title, total_subscribers, channel_link))

    return top_10_channels

if __name__ == "__main__":
    region_code = 'US'  # Replace this with the desired region code
    top_10_channels = get_top_10_channels(region_code)

    print(f"Top 10 YouTube channels in {region_code}:")
    for i, (channel_title, video_title, total_subscribers, channel_link) in enumerate(top_10_channels, start=1):
        print(f"{i}. Channel: {channel_title} | Video: {video_title} | Subscribers: {total_subscribers} | Channel Link: {channel_link}")