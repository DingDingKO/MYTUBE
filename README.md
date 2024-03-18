# MYTUBE
An alternate way to view the videos of Youtube channels you are subscribed to. Removes all the distractions of the Youtube app by instantly creating an embedded playlist of videos selected from inside a daily scheduled newsletter containing the videos released over the previous day. Also allows different list of channels to be sent, allowing for a more focused list of channels during the week and a longer list at the weekend.

The implementation could have been slightly different but I made sure that it was only made from free tier products from AWS and is the most efficent use of credits in the Youtube data API. I also had to get around the limitation of not being able to use any Javascript in the email itself.

## Pre-Setup:
* Use the Setup Tools to load the channels you are subscribed to into the channel_data.pkl and channel_data_large.pkl files (allows a different set of videos to be shown at the weekend). 
You will need a Youtube Data API key from the Google API Console. https://developers.google.com/youtube/v3/getting-started

## Setup:

2 AWS Lambda functions are needed one Sender (MYTUBE) and one Reciever (MYTUBE Reciever)

### Reciever function:
 * Setup a Function URL (in the Configuration tab)

### Sender function:
 * Setup a Layer for Pandas
 * Setup 4 Environment variables (in the Configuration tab), api_key (the API key from Youtube Data API), destination_email (the recipient of the newsletter), lambda_function_url (the Function URL of the reciever), and sender_email (the sending email address)
 * Setup a cron job for when you want to recieve the newsletter email

Both the sender and reciever email address need to be verified with AWS SNS 

<p align="center">
<img width="400" alt="Screenshot 2022-12-17 at 15 28 37" src="https://user-images.githubusercontent.com/102842055/208250004-bee20b61-8e95-474d-be8a-ccaf64768736.png"><img width="400" alt="Screenshot 2022-12-17 at 15 29 07" src="https://user-images.githubusercontent.com/102842055/208250014-5da3f7b6-a5da-4140-93c8-e62391f7e0a6.png">
</p>
