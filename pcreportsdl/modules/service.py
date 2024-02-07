"""

Uses the credentials downloaded from Gmail's API to
generate an access token for the Gmail services.

"""

import pickle
from pathlib import Path
from time import sleep

from modules import display

from googleapiclient.discovery import Resource, build
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def get_service(token_file, creds_json, scopes) -> Resource:
    """Uses the credentials downloaded from Gmail's API to
    generate an access token for the Gmail services. If one
    exists, it uses that one, if not, it creates one and saves it.

    Returns:
        Resource: Gmail services access token.
    """
    while True:
        if Path(token_file).exists():
            with open(token_file, "rb") as token:
                creds = pickle.load(token)
        else:
            creds = None

        try:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_json, scopes)
                    creds = flow.run_local_server(port=0)

                    with open(token_file, "wb") as token:
                        pickle.dump(creds, token)
        # Remove token.pickle if it has expired and try again
        except RefreshError:
            display.token_error()
            sleep(1)
            Path(token_file).unlink()
            continue

        return build("gmail", "v1", credentials=creds)
