from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.note import Note
from app.schemas.note_dto import NoteCreate, NoteUpdate

class NoteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, note: NoteCreate) -> Note:
        db_note = Note(**note.dict())
        self.db.add(db_note)
        await self.db.commit()
        await self.db.refresh(db_note)
        return db_note

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[Note]:
        result = await self.db.execute(select(Note).offset(skip).limit(limit))
        return result.scalars().all()

    async def find_by_id(self, note_id: int) -> Note | None:
        result = await self.db.execute(select(Note).filter(Note.id == note_id))
        return result.scalars().first()

    async def update(self, note_id: int, note_update: NoteUpdate) -> Note | None:
        db_note = await self.find_by_id(note_id)
        if db_note:
            update_data = note_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_note, key, value)
            await self.db.commit()
            await self.db.refresh(db_note)
        return db_note

    async def delete(self, note_id: int) -> bool:
        db_note = await self.find_by_id(note_id)
        if db_note:
            await self.db.delete(db_note)
            await self.db.commit()
            return True
        return False
