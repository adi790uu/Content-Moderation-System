from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from moderation_service.app.tasks import moderate_text_task

app = FastAPI()


class ModerationRequest(BaseModel):
    text: str


@app.post("/api/v1/moderate/text")
async def moderate_text(
    request: ModerationRequest,
    background_tasks: BackgroundTasks,
):
    try:
        background_tasks.add_task(moderate_text_task, request.text)
        return {"status": "Moderation task submitted"}
    except Exception as e:
        print(e)
