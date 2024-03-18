import json


def lambda_handler(event, context):
    raw_input = event['rawQueryString']
    and_removed = raw_input.replace('&', "")
    video_ids_list = and_removed.split('id=')

    # Since string starts "id=" the first element in video_ids_list is empty
    video_ids_string = ",".join(video_ids_list[1:])

    if video_ids_string:
        return {
            'statusCode': 302,
            'headers': {
                'Location': f'https://www.youtube.com/embed/?playlist={video_ids_string}'
            }
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('No videos selected')
        }
