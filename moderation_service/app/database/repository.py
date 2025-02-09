# from moderation_service.app.database.session import get
# from moderation_service.app.models.moderation import ModerationResult


# class ModerationRepository:
#     @staticmethod
#     async def save_moderation_result(text: str, result: list):
#         with get_session() as session:
#             moderation_entry = ModerationResult(text=text, result=str(result))
#             session.add(moderation_entry)
#             session.commit()
