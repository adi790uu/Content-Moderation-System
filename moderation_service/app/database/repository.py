from pydantic import UUID4
from app.database.session import AsyncSessionLocal, SyncSessionLocal
from app.models.moderation import ModerationResult
from sqlalchemy import select
from loguru import logger
from app.core.exceptions import RepositoryException


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
        try:
            async with AsyncSessionLocal() as session:
                stmt = select(ModerationResult).where(
                    ModerationResult.uuid == uuid,
                )
                result = await session.execute(stmt)
                moderation_result = result.scalars().first()

                if moderation_result is None:
                    logger.error("Record not found")
                    raise RepositoryException(
                        message="Record not found!",
                        status_code=404,
                    )
                return moderation_result.result
        except RepositoryException as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.error(e)
            raise RepositoryException(
                message="Error occurred fetching record from database!",
                status_code=400,
            )
