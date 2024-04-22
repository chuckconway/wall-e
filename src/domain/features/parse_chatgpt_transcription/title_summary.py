from pydantic import BaseModel


class TitleSummary(BaseModel):
    title: str = ""
    summary: str = ""