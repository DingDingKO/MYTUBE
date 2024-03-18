import asyncio
import os
import requests
import datetime
import pickle
import boto3
import numpy as np
import pandas as pd
from string import Template

MAX_RETRIES = 5
FRIDAY = 4
API_KEY = os.environ["api_key"]
MAX_RESULTS = 10


# See if video was published within cutoff
def is_video_new(df):
    return df['publishedAt'][0] > get_previous_date()


# Normalise json response and parse
def json_collapser(json_response):
    video_dfs = []

    if "items" in json_response:
        videos = json_response["items"]
        for video in videos:
            video_df = pd.json_normalize(video['snippet'], sep='_')
            if is_video_new(video_df):
                video_df.insert(4, "button", [make_image_button(video_df)])
                video_dfs.append(video_df)
    return pd.concat(video_dfs) if video_dfs else None


# Check if today is the weekend
def is_weekend():
    day_of_the_week = datetime.datetime.today().weekday()
    return day_of_the_week > FRIDAY


# Load dataframe containing data about the YouTube channels subscribed to
def get_channel_data():
    channel_data_file = 'channel_data_large' if is_weekend() else 'channel_data'
    return pickle.load(open(f'{channel_data_file}.pkl', 'rb'))


# Get the date of cut off of when to receive videos from depending on day of the week
def get_previous_date():
    days_to_search_through = 7 if is_weekend() else 1
    return ((datetime.datetime.now() - datetime.timedelta(days=days_to_search_through))
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


# Execute the REST request
def http_get_sync(url):
    response = requests.get(url)
    return response.json()


# Assign request to a thread to be executed
async def http_get(url):
    tries = 0
    while tries < MAX_RETRIES:
        try:
            return await asyncio.to_thread(http_get_sync, url)
        except:
            await asyncio.sleep(1)
            tries += 1
    raise Exception(f"{url}")


# Make a REST API request for the data from one channel playlist id
async def get_a_channel_playlist(playlist_id):
    # Request to get the last MAX_RESULTS uploaded videos' title, published time, thumbnail url, and video id
    url_request = (
        f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={MAX_RESULTS}&playlistId="
        f"{playlist_id}&fields=items(snippet(title%2CpublishedAt%2Cthumbnails(high(url))%2"
        f"CresourceId(videoId)))&key={API_KEY}")
    return playlist_id, await http_get(url_request)


# Asynchronously requests all the playlist data
async def get_all_playlists(playlist_ids):
    return await asyncio.gather(
        *[get_a_channel_playlist(playlist_id) for playlist_id in playlist_ids if playlist_id is not None])


# Collect all the videos that have been published in the last day/week
async def collect_unseen_videos(channel_data):
    all_channels_videos = await get_all_playlists(channel_data['upload_playlistId'])
    unseen_videos = [(channel_id, json_collapser(channel_videos)) for channel_id, channel_videos in all_channels_videos]
    return [(playlist_id, df) for playlist_id, df in unseen_videos if df is not None]


# Make an HTML Button from the video thumbnail to be used in a form
def make_image_button(table_contents):
    video_id = table_contents["resourceId_videoId"][0]
    video_thumbnail_source = table_contents["thumbnails_high_url"][0]
    return f'''<li><input type="checkbox" id="{video_id}" name = "id" value="{video_id}"/><label for="{video_id}"><img src="{video_thumbnail_source}" /></label></li>'''


# Create an HTML table containing all the available videos a channel has
def make_table(channel_title, df):
    return f"<br><h1>{channel_title}</h1>{df.to_html(header=False, escape=False, index=False)}"


# Find the title of the channel the playlist belongs to
def find_title(channel_data, playlist_id):
    playlist_Id_column = channel_data['upload_playlistId']
    return playlist_Id_column.index[np.where(playlist_Id_column == playlist_id)].tolist()[0]


# Load HTML template
def load_template(file_path):
    with open(file_path, "r") as file:
        template = file.read()
    # Have to use Template to stop confusion between CSS
    return Template(template)


# Fill HTML template with content
def fill_template(template, **kwargs):
    return template.substitute(**kwargs)


# Build HTML tables to be displayed
def build_tables(unseen_videos, channel_data):
    html_body = []
    # Add each Title/Thumbnail image button to a table
    for channel_id, df in unseen_videos:
        title = find_title(channel_data, channel_id)
        html_body.append(make_table(title, df.loc[:, ['button', 'title']]))
    return ''.join(html_body)


# Build the HTML content of the email
def build_website(content):
    html_template = load_template("email.html")
    content_to_add = {"lambda_function_url": os.environ['lambda_function_url'],
                      "tables": content
                      }
    return fill_template(html_template, **content_to_add)


# Send an email using the AWS SES service
def send_email(payload):
    SENDER_EMAIL = os.environ['sender_email']
    DESTINATION_EMAIL = os.environ['destination_email']

    ses = boto3.client('ses')
    ses.send_email(Source=SENDER_EMAIL, Destination={'ToAddresses': [DESTINATION_EMAIL]},
                   Message={'Subject':
                                {'Data': f"My Tube: " + datetime.datetime.now().strftime("%d/%m/%Y"),
                                 'Charset': 'UTF-8'},
                            'Body':
                                {'Html': {'Data': payload, 'Charset': 'UTF-8'}}
                            })


def lambda_handler(event, context):
    channel_data = get_channel_data()
    unseen_videos = asyncio.run(collect_unseen_videos(channel_data))
    tables_content = build_tables(unseen_videos, channel_data)
    website_html = build_website(tables_content)
    send_email(website_html)


if __name__ == '__main__':
    lambda_handler(1, 1)
