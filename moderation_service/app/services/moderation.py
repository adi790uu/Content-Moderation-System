from app.core.deps import get_db
import app.external.openai as openai_service


class ModerationService:
    async def __init__(self):
        self.db = await get_db()
        pass

    def moderate_text(text: str):
        result = openai_service.moderate_text(text=text)
        return result
