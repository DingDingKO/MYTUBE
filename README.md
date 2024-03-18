# MYTUBE
An alternate way to view the videos of Youtube channels you are subscribed to. Removes the distractions of ... by allowing you to select videos that you want to watch .... 

Utilises the functionality of 

*Pre-Setup:
Use the Setup Tools to load the channels you are subscribed to into the channel_data.pkl and channel_data_large.pkl files (allows a different set of videos to be shown at the weekend). 
You will need a Youtube Data API key from the Google API Console. https://developers.google.com/youtube/v3/getting-started

* Setup:
 2 AWS Lambda functions are needed one Sender (MYTUBE) and one Reciever (MYTUBE Reciever)

Reciever function:
 Setup a Function URL (in the Configuration tab)

Sender function:
 Setup a Layer for Pandas
 Setup 4 Environment variables (in the Configuration tab), api_key (the API key from Youtube Data API), destination_email (the recipient of the newsletter), lambda_function_url (the Function URL of the reciever), and sender_email (the sending email address)

 Both the sender and reciever email address need to be verified with SNS 

<p align="center">
<img width="400" alt="Screenshot 2022-12-17 at 15 28 37" src="https://user-images.githubusercontent.com/102842055/208250004-bee20b61-8e95-474d-be8a-ccaf64768736.png"><img width="400" alt="Screenshot 2022-12-17 at 15 29 07" src="https://user-images.githubusercontent.com/102842055/208250014-5da3f7b6-a5da-4140-93c8-e62391f7e0a6.png">
</p>
