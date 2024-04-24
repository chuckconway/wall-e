from pydantic import BaseModel


class SummaryMetadata(BaseModel):
    title: str = ""
    summary: str = ""
    filename: str
