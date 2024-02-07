"""

Uses Gmail Services/API to search the user's mailbox for messages 
matching the specified tags, and returns a list of the messages it finds and 
prints the number found to the console.

"""


from googleapiclient.discovery import Resource


def find_matching_messages(service: Resource, tags: str) -> list:
    """Uses Gmail Services/API to search the user's mailbox for messages
    matching the specified tags, and returns a list of the messages it finds.

    Args:
        service (Resource): Gmail services/API access resource
        tags (str): String of Gmail tags to search mailbox for matches of

    Returns:
        list: List of messages matching the specified tags
    """

    matches = (
        service.users()
        .messages()
        .list(userId="me", q=tags)
        .execute()
        .get("messages", [])
    )

    return matches
