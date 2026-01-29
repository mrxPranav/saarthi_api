from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.services.note_service import NoteService
from app.repositories.note_repository import NoteRepository
from app.services.ai_service import GroqService
from app.schemas.ai_dto import AIRequest, AIResponse

router = APIRouter(prefix="/ai", tags=["AI Operations"])

def get_note_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    repository = NoteRepository(db)
    return NoteService(repository)

def get_ai_service() -> GroqService:
    return GroqService()

@router.post("/generate-title/{note_id}")
async def generate_title_for_note(
    note_id: int, 
    service: NoteService = Depends(get_note_service),
    ai_service: GroqService = Depends(get_ai_service)
):
    updated_note = await service.update_note_title_with_ai(note_id, ai_service)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Title updated", "note": updated_note}

@router.post("/generate-titles/all")
async def generate_titles_for_all_notes(
    service: NoteService = Depends(get_note_service),
    ai_service: GroqService = Depends(get_ai_service)
):
    updated_count = await service.update_all_notes_titles_with_ai(ai_service)
    return {"message": f"Updated {updated_count} notes"}

@router.post("/generate-titles/today")
async def generate_titles_for_today(
    service: NoteService = Depends(get_note_service),
    ai_service: GroqService = Depends(get_ai_service)
):
    updated_count = await service.update_todays_notes_titles_with_ai(ai_service)
    return {"message": f"Updated {updated_count} notes created today"}

@router.post("/chat", response_model=AIResponse)
async def chat_with_ai(
    request: AIRequest,
    ai_service: GroqService = Depends(get_ai_service)
):
    try:
        response_data = await ai_service.get_custom_completion(request.system_prompt, request.user_prompt)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
