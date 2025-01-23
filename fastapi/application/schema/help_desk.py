from pydantic import BaseModel

class HelpDesk(BaseModel):
    """
    Represents the request payload for submitting a help request.

    Attributes:
        text (str): The message or description provided by the user seeking assistance.
    """
    text: str


class ResponseHelp(BaseModel):
    """
    Represents the response object for a successfully created help request.

    Attributes:
        id (str): A unique identifier for the help request.
    """
    id: str


class Report(BaseModel):
    """
    Represents the request payload for submitting an issue or problem report.

    Attributes:
        text (str): The message or description of the issue provided by the user.
    """
    text: str


class ReportResponse(BaseModel):
    """
    Represents the response object for a successfully created problem report.

    Attributes:
        id (str): A unique identifier for the problem report.
    """
    id: str
