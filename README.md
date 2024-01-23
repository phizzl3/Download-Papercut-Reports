# Download-Papercut-Reports

Download PaperCut reports using Gmail API

This is written specifically for my use case and works while logged 
in as a single user to download reports from a Gmail account. 

Additional requirements:

* Gmail API will need to be enabled on account
* credentials.json file from Gmail (Downloaded) (stored in ./private)
* token.pickle file from Gmail (Generated) (stored in ./private)
* data.py file containing search tags (stored in ./private)  

Instructions for the above can be found at:  
https://developers.google.com/gmail/api/quickstart/python

What it does:

* Connects to Gmail API
* Checks for credentials & token
  * Generates token if it doesn't exist using credentials from Gmail
* Searches Gmail for Unread messages from PaperCut with attachments
* Gets all of those messages
* Downloads and renames the attachments based on location
* Outputs the attachments to a folder based on report date located
  in the user's Home / Downloads folder
* Marks messages Read and Archives them when done

Big thanks to **BW1ll** (https://github.com/BW1ll) for helping figure out 
and for writing a big chunk of this code! 

Requirements: 

* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib

```bash
$ pip install -r requirements.txt
```
