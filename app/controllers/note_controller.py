from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.schemas.note_dto import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import NoteService
from app.repositories.note_repository import NoteRepository

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_note_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    repository = NoteRepository(db)
    return NoteService(repository)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.create_note(note)

@router.get("/", response_model=List[NoteResponse])
async def read_notes(skip: int = 0, limit: int = 100, service: NoteService = Depends(get_note_service)):
    return await service.get_all_notes(skip, limit)

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, service: NoteService = Depends(get_note_service)):
    db_note = await service.get_note_by_id(note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note_update: NoteUpdate, service: NoteService = Depends(get_note_service)):
    updated_note = await service.update_note(note_id, note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, service: NoteService = Depends(get_note_service)):
    success = await service.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return
