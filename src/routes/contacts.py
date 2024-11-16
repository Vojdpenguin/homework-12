from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts")


@router.get("/filter", response_model=list[ContactResponse])
async def filter_contacts(name: Optional[str] = Query(None, description="Фільтр за імям"),
                          surname: Optional[str] = Query(None, description="Фільтр за прізвищем"),
                          email: Optional[str] = Query(None, description="Фільтр за email"),
                          db: Session = Depends(get_db)):
    contacts = await repository_contacts.filter_contacts(name, surname, email, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контакти не знайдені")
    return contacts

@router.get("/birthday", response_model=List[ContactResponse])
async def get_birthday_contracts(db:Session = Depends(get_db)):
    contacts = await repository_contacts.get_birthday_contacts(db)
    return contacts


@router.get("/", response_model=List[ContactResponse])
async def check_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def check_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def contact_create(body: ContactCreate, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def contact_update(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def contact_remove(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact


