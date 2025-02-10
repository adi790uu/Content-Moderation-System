from pydantic import BaseModel


class ModerateTextPayload(BaseModel):
    text: str
