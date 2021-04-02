#!/usr/bin/env python3
"""
See README.md for info
"""

import base64
import pickle
import re
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Contains the tags needed to find the messages
from private.data import QUERY


# These are the access "Scopes" that this application will
# have to the Gmail account. (Read and modify Messages)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# Access token downloaded from Gmail API (don't share)
TOKENFILE = Path(__file__).resolve().parent / 'private' / 'token.pickle'
# Credentials file downloaded from Gmail API (don't share)
CREDSJSON = Path(__file__).resolve().parent / 'private' / 'credentials.json'


# Regex search patterns for subject line in emails
# School name
EXECUTIVE_SUM_RE = re.compile(r'(:\s(.+)\sE)')
# Printer groups
PRINTER_GRP_RE = re.compile(r'(P[a-z].+- (s[a-z]{6}[A-Z]{3}?|s[a-z]{6}))')
# Report date
REPORT_DT_RE = re.compile(r'(([A-Z][a-z]{2})\s\d,\s(\d{4}))')


class Gmail:
    """
    Object initialization and a couple of methods for working with 
    Gmail for downloading messages and PaperCut attachments and 
    editing tags.
    """

    def __init__(self):
        """
        Initialize Gmail object - Gets Gmail credentials and access 
        token and uses them to build an access service instance for 
        Gmail account.
        """

        # Reset variable
        creds = None

        # The file token.pickle stores the user's access and refresh
        # tokens, and is created automatically when the authorization
        # flow completes for the first time.
        if Path(TOKENFILE).exists():
            with open(TOKENFILE, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the
        # user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDSJSON, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(TOKENFILE, 'wb') as token:
                pickle.dump(creds, token)

        # Build the service needed to access the Gmail account
        self.service = build('gmail', 'v1', credentials=creds)

    def get_messages(self):
        """
        Uses Gmail service to pull a list of email messages based 
        on a specified search query.

        Returns:
            self
        """

        # Use Gmail service to request messages matching 'QUERY'
        results = self.service.users().messages().list(
            userId='me',
            q=QUERY
        ).execute()

        # Add list of messages to 'messages' attribute or blank list
        # if none found.
        self.messages = results.get('messages', [])

        # Display total matching messages found to console
        print(f'\n Total messages found: {len(self.messages)}\n')

        # Display message to console if no matching messages are found
        if not self.messages:
            input('\n No messages found. ENTER to close...')

        return self

    def get_attachments(self):
        """
        Searches attached messages details for subject line and 
        attachments. Downloads and renames the located attachments 
        based on subject and filename, and saves to a specified output 
        (Downloads/{Date}) folder. Marks each message as Read and 
        archives when done downloading. 

        Returns:
            self
        """

        # Check to make sure object has 'messages' attribute and
        # call 'get_messages' method if it's missing
        if not hasattr(self, 'messages'):
            self.get_messages()

        # Run only if the messages attribute list isn't empty
        if self.messages:
            try:
                # Loop through individual messages to access
                # contents/payload
                for message in self.messages:
                    message_details = self.service.users().messages().get(
                        userId='me',
                        id=message['id']
                    ).execute()

                    # Set a couple of quick variables to save
                    # some typing later.
                    # Payload is where the majority of the
                    # good stuff is.
                    # Parts is where the attachments info is
                    payload = message_details['payload']
                    subject = payload['headers'][21]['value']
                    message_parts = payload['parts']

                    # Reset variables needed for next step for
                    # additional loops
                    executive_summary, printer_groups, name_part = 0, 0, 0

                    # Search subject line for Regex patterns
                    executive_summary = EXECUTIVE_SUM_RE.search(subject)
                    printer_groups = PRINTER_GRP_RE.search(subject)
                    report_date = REPORT_DT_RE.search(subject)

                    # Dictionary used to get month number to match
                    # current folder-naming structure for output.
                    # ex: '01 Jan 20'
                    months = {'Jan': '01', 'Feb': '02', 'Mar': '03',
                              'Apr': '04', 'May': '05', 'Jun': '06',
                              'Jul': '07', 'Aug': '08', 'Sep': '09',
                              'Oct': '10', 'Nov': '11', 'Dec': '12'}

                    # Generate ouput folder name
                    folder_name = (f'{months.get(report_date.group(2))} '
                                   f'{report_date.group(2)} '
                                   f'{report_date.group(3)[2:]}')

                    # Check for output folder in user's
                    # Home / 'Downloads' folder,
                    # create if doesn't exist and set as target directory
                    Path.mkdir(Path.home() / 'Downloads' / folder_name,
                               exist_ok=True)
                    out_directory = f'{Path.home()}/Downloads/{folder_name}/'

                    # Set output name part variable based on which
                    # Regex is found
                    if executive_summary:
                        name_part = executive_summary.group(2)
                    elif printer_groups:
                        name_part = printer_groups.group(1)

                    # Use Gmail service to get (encoded) attachment
                    # data and set variable
                    attachment = (
                        self.service.users().messages().attachments().get(
                        userId='me',
                        messageId=message['id'],
                        id=message_parts[1]['body']['attachmentId']
                    ).execute()
                    )

                    # Decode attachment data and set variable
                    output_file = base64.urlsafe_b64decode(
                        attachment['data'].encode('UTF-8'))

                    # Combine expression from subject with filename
                    # for output file
                    out_file = f"{name_part} {message_parts[1]['filename']}"

                    # Save attachment to folder with new filename and
                    # print to console
                    with open(f'{out_directory}{out_file}', 'wb') as f:
                        f.write(output_file)
                        print(f' {out_file} as been created')

                    # Mark message as read and archive (remove labels)
                    # and print to console
                    self.service.users().messages().modify(
                        userId='me',
                        id=message.get('id'),
                        body={'removeLabelIds': ['UNREAD', 'INBOX']}
                    ).execute()
                    print(' Marked as Read and Archived.')

            except Exception as e:
                print(f' An error has occurred: \n {e}')

        return self


def get_reports():
    """
    Generate Gmail object and call methods to get email 
    messages and needed attachments for file output.
    """

    print('\n This downloads and saves PaperCut attachments from UNREAD '
          'messages in the CopierSupport INBOX.\n Messages NOT marked UNREAD '
          'or located outside the INBOX will be ignored.\n Files output to '
          '"User/Downloads/" folder by date.')
    input('\n Press ENTER to continue...')

    email = Gmail()
    email.get_messages().get_attachments()


if __name__ == "__main__":
    get_reports()
