from app.repositories.note_repository import NoteRepository
from app.schemas.note_dto import NoteCreate, NoteUpdate, NoteResponse
from app.models.note import Note
from app.services.ai_service import GroqService

class NoteService:
    def __init__(self, repository: NoteRepository):
        self.repository = repository

    async def create_note(self, note: NoteCreate) -> NoteResponse:
        return await self.repository.save(note)

    async def get_all_notes(self, skip: int = 0, limit: int = 100) -> list[NoteResponse]:
        return await self.repository.find_all(skip, limit)

    async def get_note_by_id(self, note_id: int) -> NoteResponse | None:
        return await self.repository.find_by_id(note_id)

    async def update_note(self, note_id: int, note: NoteUpdate) -> NoteResponse | None:
        return await self.repository.update(note_id, note)

    async def delete_note(self, note_id: int) -> bool:
        return await self.repository.delete(note_id)

    async def update_note_title_with_ai(self, note_id: int, ai_service: GroqService) -> NoteResponse | None:
        db_note = await self.repository.find_by_id(note_id)
        if not db_note:
            return None
        
        new_title = await ai_service.generate_title(db_note.note)
        db_note.title = new_title
        await self.repository.db.commit()
        await self.repository.db.refresh(db_note)
        return db_note

    async def update_all_notes_titles_with_ai(self, ai_service: GroqService) -> int:
        notes = await self.repository.get_all_notes_no_limit()
        updated_count = 0
        for note in notes:
            if not note.title:
                new_title = await ai_service.generate_title(note.note)
                note.title = new_title
                updated_count += 1
        
        if updated_count > 0:
            await self.repository.db.commit()
        return updated_count

    async def update_todays_notes_titles_with_ai(self, ai_service: GroqService) -> int:
        notes = await self.repository.find_created_today()
        updated_count = 0
        for note in notes:
            if not note.title:
                new_title = await ai_service.generate_title(note.note)
                note.title = new_title
                updated_count += 1
        
        if updated_count > 0:
            await self.repository.db.commit()
        return updated_count
