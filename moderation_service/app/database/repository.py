from app.database.session import SyncSessionLocal
from app.models.moderation import ModerationResult


class ModerationRepository:
    @staticmethod
    def save_moderation_result(text: str, result: bool, meta: str):
        with SyncSessionLocal() as session:
            moderation_result = ModerationResult(
                text=text,
                result=result,
                meta=meta,
            )
            session.add(moderation_result)
            session.commit()
