"""

Class for generating Message objects and their associated attributes.

"""


from googleapiclient.discovery import Resource
from modules.settings import REPORT_DT_RE, EXECUTIVE_SUM_RE, PRINTER_GRP_RE


class Message:
    """Class for generating Message objects and their associated attributes."""

    def __init__(self, service: Resource, message_info: dict) -> None:
        self.message_details = (
            service.users().messages().get(userId="me", id=message_info["id"]).execute()
        )

    @property
    def subject(self) -> str:
        """Locates and returns the subject line from the message.

        Returns:
            str: Message's subject line.
        """
        for header in self.message_details["payload"]["headers"]:
            if header["name"] == "Subject":
                return header["value"]

        return "No Subject"

    @property
    def attachments_list(self) -> list:
        """Generates a list of the message's attachment filenames.

        Returns:
            list: List of filenames for the message's attachments.
        """
        attachment_names = []
        for each in self.message_details["payload"]["parts"]:
            if each["filename"]:
                attachment_names.append(each["filename"])

        return attachment_names

    @property
    def folder_name(self) -> str:
        """Generates and returns a formatted folder name to output
        the final files.

        Returns:
            str: Formatted folder name.
        """
        found = REPORT_DT_RE.search(self.subject)
        return f"{found[2]}-{found[3]}"

    @property
    def executive_summary_prefix(self) -> str:
        """Searches for the Executive Summary information in the subject.

        Returns:
            str: School name executive summary
        """
        found = EXECUTIVE_SUM_RE.search(self.subject)
        if found:
            return EXECUTIVE_SUM_RE.search(self.subject)[2]

    @property
    def printer_groups_prefix(self) -> str:
        """Searches for Printer Groups information in the subject.

        Returns:
            str: Printer group summary
        """
        found = PRINTER_GRP_RE.search(self.subject)
        if found:
            return PRINTER_GRP_RE.search(self.subject)[0]
