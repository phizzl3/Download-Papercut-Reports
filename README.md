# Papercut-Reports-Downloader

Download PaperCut reports using Gmail API

This is written specifically for my use case and works while logged
in as a single user to download reports from a Gmail account.

## Additional requirements

* Gmail API will need to be enabled on account
* credentials.json file from Gmail (Downloaded) (copy to ~/PyAppFiles/Papercut Reports Downloader)
* token.pickle file from Gmail (Generated) (stored in same directory as above)
* config.json file containing search tags, etc (generated on first run in same directory as above)
  * The above config file will need to be updated in order for the program to work correctly.  

Instructions for the above can be found at:  
<https://developers.google.com/gmail/api/quickstart/python>

## What it does

* Connects to Gmail API
* Checks for credentials & token
  * Generates token if it doesn't exist using credentials from Gmail
* Searches Gmail for messages based on query in config.json
* Gets all of those messages
* Downloads and renames the attachments based on location
* Outputs the attachments to a folder based on report date located
  in the ~/Downloads folder
* Optionally marks messages Read and Archives them when done

## Requirements

* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib
* tqdm
* pyinstaller

## Build info

Windows

```bash
pyinstaller -F -n "Papercut Reports Downloader" --icon=.\icon\pcut.ico .\pcreportsdl\main.py
```

MacOS

```bash
pyinstaller -F -n "Papercut Reports Downloader" ./pcreportsdl/main.py
```
