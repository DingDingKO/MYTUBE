import pickle
import pandas as pd
import boto3
import datetime

from apiclient.discovery import build

api_key = 'API_KEY'##########ADD KEY########### API_KEY

youtube = build('youtube','v3',developerKey=api_key)

def json_collapser(dict_of_dicts):
    new_dict = {}

    for item in dict_of_dicts:
        
        name = item['snippet']['title']
    
        df = pd.json_normalize(item['snippet'], sep='_')

        values = df.to_dict(orient='records')[0]
        new_dict[name] = values
        
    channel_data_frame = pd.DataFrame(new_dict).T
    del channel_data_frame['title']
    return channel_data_frame
    
def find_new_videos(upload_id, time_to_search_from):
    if upload_id == None:
        return None
    
    get_last_ten_videos_from_channel = youtube.playlistItems().list(part='snippet', maxResults=10, playlistId=upload_id, fields = ('items(snippet(title,publishedAt,thumbnails(high(url)),resourceId(videoId))),,nextPageToken'))

    response = get_last_ten_videos_from_channel.execute()
    videos_json = response['items']

    videos_df = json_collapser(videos_json)
    
    unwatched_videos = videos_df[videos_df['publishedAt'] > time_to_search_from]
    
    if unwatched_videos.empty:
        return None
    else:
        unwatched_videos['thumbnails_high_url'] = unwatched_videos.iloc[:,1:].apply(make_image_button, axis=1)
        return unwatched_videos
    
def make_image_button(table_contents):
    # Makes HTML Button of the video thumbnail
    video_thumbnail_source = table_contents[0]
    video_id = table_contents[1]
    
    return '''<li><input type="checkbox" id="''' + video_id + '''" name = "id" value="'''+ video_id +'''"/><label for="''' + video_id + '''"><img src="''' + video_thumbnail_source + '''" /></label></li>'''

def send_email(payload):
    # Email
    ses = boto3.client('ses')


        
    ##################### ADD EMAILS ####################### SENDER_EMAIL, RECIPIENT_EMAIL
    ses.send_email(Source = 'SENDER_EMAIL', Destination = {'ToAddresses': ['RECIPIENT_EMAIL']},
	    Message = {'Subject': {'Data': "My Tube: "+ datetime.datetime.now().strftime("%d/%m/%Y"), 'Charset': 'UTF-8'},
		    'Body': {'Html':{'Data': payload, 'Charset': 'UTF-8'}}})

def build_website(unseen_videos):
    # HTML
    html_head, html_tail = pickle.load(open('website_HTML_MYTUBE.pkl','rb'))

    # Adds each Title/Thumbnail image Button to the website
    for channel_title in unseen_videos.keys():
        html_head += '<br><h1>'+ channel_title +'</h1>'+ pd.DataFrame(unseen_videos[channel_title].iloc[:,-2]).to_html(header=False,escape=False)

    return html_head + html_tail

def lambda_handler(event, context):
    
    # Load Subscribed Channels
    channel_data = pickle.load(open('channel_data.pkl','rb'))

    day_of_the_week = datetime.datetime.today().weekday()
    friday = 4
    weekend = day_of_the_week > friday


    if weekend:
        channel_data = pickle.load(open('channel_data_large.pkl','rb'))
        days_to_search_through = 7
        
    else:
    	days_to_search_through = 1

    date_to_search_from = (datetime.datetime.now() - datetime.timedelta(days = days_to_search_through)).strftime("%Y-%m-%dT%H:%M:%SZ")

    
    unseen_videos = channel_data['upload_playlistId'].apply(find_new_videos, time_to_search_from = date_to_search_from)
    # Remove if no new videos from channel
    unseen_videos = unseen_videos.dropna()

    website_html = build_website(unseen_videos)
    send_email(website_html)
