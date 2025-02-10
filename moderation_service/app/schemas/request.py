from pydantic import BaseModel


class ModerateTextPayload(BaseModel):
    text: str


class ModerateTextRequest(BaseModel):
    text: str
