from pydantic import UUID4
from app.database.session import AsyncSessionLocal, SyncSessionLocal
from app.models.moderation import ModerationResult
from sqlalchemy import select


class ModerationRepository:
    @staticmethod
    def save_moderation_result(
        text: str, result: bool, meta: str, moderation_id: UUID4
    ):
        with SyncSessionLocal() as session:
            moderation_result = ModerationResult(
                uuid=moderation_id,
                text=text,
                result=result,
                meta=meta,
            )
            session.add(moderation_result)
            session.commit()

    async def get_moderation_result_by_uuid(uuid: UUID4):
        async with AsyncSessionLocal() as session:
            stmt = select(ModerationResult).where(
                ModerationResult.uuid == uuid,
            )
            result = await session.execute(stmt)
            return result.scalars().first()
