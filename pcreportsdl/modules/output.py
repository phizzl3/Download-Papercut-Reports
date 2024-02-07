"""

Module containing functions for outputting message body and attachments.

"""

import base64

from googleapiclient.discovery import Resource
from modules.settings import OUTFOLDER


def write_msg_attachments(service: Resource, message_obj) -> None:
    """Gets, decodes, and outputs the message's attachments to the
    target folder.

    Args:
        service (Resource): Gmail API service
        message_obj (Message): Message object
    """
    for each in message_obj.message_details["payload"]["parts"]:
        if each["filename"] in message_obj.attachments_list:
            pid = int(each["partId"])
            # Gets encoded attachments
            encoded = (
                service.users()
                .messages()
                .attachments()
                .get(
                    userId="me",
                    messageId=message_obj.message_details["id"],
                    id=message_obj.message_details["payload"]["parts"][pid]["body"][
                        "attachmentId"
                    ],
                )
                .execute()
            )
            # Decodes the attachment data
            decoded = base64.urlsafe_b64decode(encoded["data"].encode("UTF-8"))
            # Sets the ouptut folder
            output_folder = OUTFOLDER / message_obj.folder_name
            if not output_folder.exists():
                output_folder.mkdir(parents=True)
            # Sets the filename for school executive summaries
            if message_obj.executive_summary_prefix:
                filename = f"{message_obj.executive_summary_prefix}.pdf"
            else:
                filename = each["filename"]
            # Outputs decoded/named files
            with open(output_folder / filename, "wb") as f:
                f.write(decoded)
