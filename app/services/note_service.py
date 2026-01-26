from app.repositories.note_repository import NoteRepository
from app.schemas.note_dto import NoteCreate, NoteUpdate, NoteResponse
from app.models.note import Note

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
