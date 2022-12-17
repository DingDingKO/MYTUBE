# MYTUBE
An email 'newsletter' which emails me a list of my youtube subscriptions at 8am for me to select the ones I want to watch, then sends the selected videos in a playlist at 6pm. Hosted on AWS Lambda.


* At 8am, an Email with videos from the last 24 hours (or 7 days from a larger list of channels at weekends) is sent. Each video can be selected by clicking on the thumbnail.

<p align="center">
<img width="400" alt="Screenshot 2022-12-17 at 15 28 37" src="https://user-images.githubusercontent.com/102842055/208250004-bee20b61-8e95-474d-be8a-ccaf64768736.png"><img width="400" alt="Screenshot 2022-12-17 at 15 29 07" src="https://user-images.githubusercontent.com/102842055/208250014-5da3f7b6-a5da-4140-93c8-e62391f7e0a6.png">
</p>

* After pressing send, the video ids of the selected videos are compiled into an email to be sent back to the sender email.

<p align="center">
<img width="496" alt="Screenshot 2022-12-17 at 15 29 31" src="https://user-images.githubusercontent.com/102842055/208250020-8d2cb5ed-6368-48a2-890f-6de9164c7ec4.png">
</p>

* At 6pm, another email is sent which contains a link to a youtube playlist with the selected videos in it.

<p align="center">
<img width="370" alt="Screenshot 2022-12-17 at 16 01 35" src="https://user-images.githubusercontent.com/102842055/208250735-9b51bec4-1a19-4a65-a98c-037a4dc7268e.png"><img width="640" alt="Screenshot 2022-12-17 at 15 57 25" src="https://user-images.githubusercontent.com/102842055/208250731-4b1bf05b-243a-4e91-ac9f-0f6cd558ab36.png">
</p>

(By the way, I'm rubbish at CSS so I just asked ChatGPT to design me somthing cool for the background)
