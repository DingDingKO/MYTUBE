import datetime

from googleapiclient.discovery import build
import pickle
import base64
import boto3


def get_most_recent_message(messages, service):
    previous_day = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")
    email_sent_date = previous_day

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'Date':
                    date = d['value']
                    email_sent_date = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime(
                        "%Y-%m-%d %H:%M:%S")

            # Printing the subject, sender's email and message

            ###### ADD EMAIL ####### RECIPIENT_EMAIL_SIGNATURE i.e. Name <email>
            if "RECIPIENT_EMAIL_SIGNATURE" == sender and email_sent_date > previous_day:

                data = payload['body']['data']
                decoded_data = base64.b64decode(data)

                string_data = decoded_data.decode('utf-8')
                video_ids = ",".join([i[3:].strip() for i in string_data.splitlines() if i.startswith("id=")])
                if video_ids:
                    return "https://www.youtube.com/embed/?playlist=" + video_ids
        except:
            print(sender)
            return

    return


def send_email(payload):
    # Email
    ses = boto3.client('ses')
    ##################### ADD EMAILS ####################### SENDER_EMAIL, RECIPIENT_EMAIL
    ses.send_email(Source='SENDER_EMAIL', Destination={'ToAddresses': ['RECIPIENT_EMAIL']},
                   Message={'Subject': {'Data': "My Tube Playlist: " + datetime.datetime.now().strftime("%d/%m/%Y"),
                                        'Charset': 'UTF-8'},
                            'Body': {'Html': {'Data': payload, 'Charset': 'UTF-8'}}})


def lambda_handler(event, context):
    with open('token.pkl', 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(maxResults=5, userId='me').execute()
    messages = result.get('messages')

    url_content = get_most_recent_message(messages, service)

    if len(url_content) > 0:
        HTML_head, HTML_tail = pickle.load(open('website_HTML_MYTUBE_Receiver.pkl','rb'))
        website = HTML_head+url_content+HTML_tail
        send_email(website)
