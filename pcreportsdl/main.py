"""

This program uses the Gmail API to search for and download 
attachments sent by Papercut MF.

"""

__version__ = "2.0.0"

import time

from tqdm import tqdm

from modules import display
from modules.findmsg import find_matching_messages
from modules.message import Message
from modules.output import write_msg_attachments
from modules.screenclr import clearscreen
from modules.service import get_service
from modules.settings import TOKEN, CREDS, SCOPES, QUERY, ARCHIVE


class Main:
    def __init__(self):
        self.service = None
        self.matches = []
        self.message_objects = []

    def set_service(self):
        """Gets Gmail API service"""
        self.service = get_service(TOKEN, CREDS, SCOPES)

    def set_matches(self) -> list:
        """Get Messages matching the query"""
        self.matches = find_matching_messages(self.service, QUERY)

    def set_message_objects(self) -> list:
        """Gets Message objects generated from matches"""
        self.message_objects = [Message(self.service, match) for match in self.matches]


def find_and_output_files(main) -> None:
    """Finds matching messages and outputs the attached files"""
    if not main.message_objects:
        return
    print(" Downloading message data.")
    for message in tqdm(main.message_objects):
        write_msg_attachments(main.service, message)


def archive_messages(main) -> None:
    """Marks messages as READ and removes them from the INBOX."""
    if not main.message_objects:
        return
    print(" Archiving messages.")
    for match in tqdm(main.matches):
        # Mark message as read and archive (remove labels)
        main.service.users().messages().modify(
            userId="me",
            id=match.get("id"),
            body={"removeLabelIds": ["UNREAD", "INBOX"]},
        ).execute()


main = Main()
display.ascii_art(__version__)
print(" Connecting to Gmail API.")
main.set_service()
print(" Searching for matching messages.")
main.set_matches()
print(f" Matching messages found: {len(main.matches)}")
main.set_message_objects()
find_and_output_files(main)
if ARCHIVE:
    archive_messages(main)
print(" Done.")
time.sleep(2)
