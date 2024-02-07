"""

Load (use defaults first if not found) json data from
file, and use that data to generate a settings file for import.

"""

import re
from pathlib import Path

from modules.loadjsondata import loadjson
from modules.pathcheck import check_paths


# External file locations
APPFILES = Path().home() / "PyAppFiles" / "Papercut Reports Downloader"
CONFIGJSON = APPFILES / "config.json"
CREDS = APPFILES / "credentials.json"
TOKEN = APPFILES / "token.pickle"

# Output folder for downloaded files
OUTFOLDER = Path().home() / "Downloads"

# Default values for json data
DEFAULTS = {
    "query comments": [
        "This query is what will be used to search for the desired email data.",
        "You will need to update this info to match your desired search.",
        "Specifically, check the email address and update accordingly.",
        "To search for All matching messages, use the following:",
        "from:papercut@UPDATE_ME.org has:attachment",
        "To search for Unread Only matches, use the following:",
        "label:UNREAD from:papercut@UPDATE_ME.org has:attachment",
    ],
    "query": "label:INBOX from:papercut@UPDATE_ME.COM has:attachment",
    "scopes comments": [
        "These are the access 'Scopes' that this application will",
        "have to the Gmail account. (Read and modify Messages)",
        "These likely won't need to be changed, but if they are",
        "you will need to delete the file token.pickle and reload.",
    ],
    "scopes": "https://www.googleapis.com/auth/gmail.modify",
    "archive messages comments": [
        "true/false flag determining whether messages are to be archived",
        "after the files are downloaded.",
    ],
    "archive messages": False,
    "regex patterns comments": [
        "These are the Regular Expression search patterns for the project.",
        "These won't change unless reporting format from Papercut does.",
    ],
    "school reports": "(Automated report: )([A-Za-z]+(\\s*[A-Za-z]+)+ Executive summary)",
    "printer groups": "(Automated report: )(([A-Za-z]+\\s)+)-\\s+[A-Za-z]+",
    "report date": "(([A-Z][a-z]{2})\\s\\d,\\s(\\d{4}))",
}

# Load (or set defaults) settings json data
config = loadjson(CONFIGJSON, default_data=DEFAULTS)

# Verify credentials file exists
check_paths(CREDS)

# Load additional config info from json data
QUERY = config["query"]
SCOPES = [config["scopes"]]
EXECUTIVE_SUM_RE = re.compile(config["school reports"])
PRINTER_GRP_RE = re.compile(config["printer groups"])
REPORT_DT_RE = re.compile(config["report date"])
ARCHIVE = config["archive messages"]
