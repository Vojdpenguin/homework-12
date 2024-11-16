from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contacts
from src.schemas import ContactCreate, ContactUpdate
from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contacts]:
    return db.query(Contacts).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contacts:
    return db.query(Contacts).filter(Contacts.id == contact_id).first()


async def create_contact(body: ContactCreate, db: Session) -> Contacts:
    contact = Contacts(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(note_id: int, body: ContactUpdate, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == note_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def filter_contacts(name: Optional[str], surname: Optional[str], email: Optional[str], db: Session) -> list[
    Contacts]:
    conditions = []
    if name:
        conditions.append(Contacts.name.ilike(f'%{name}%'))
    if surname:
        conditions.append(Contacts.surname.ilike(f'%{surname}%'))
    if email:
        conditions.append(Contacts.email.ilike(f'%{email}%'))
    if not conditions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Мінімум один фільтр повинен бути заданий")

    return db.query(Contacts).filter(*conditions).all()


async def get_birthday_contacts(db: Session) -> list[Contacts]:
    today = datetime.today().date()
    seven_days_later = today + timedelta(days=7)

    today_day_of_year = func.extract('doy', today)
    seven_days_later_day_of_year = func.extract('doy', seven_days_later)

    query = db.query(Contacts).filter(
        or_(
            and_(
                func.extract('doy', Contacts.birthday) >= today_day_of_year,
                func.extract('doy', Contacts.birthday) <= seven_days_later_day_of_year
            ),
            func.extract('doy', Contacts.birthday) < (seven_days_later_day_of_year - 365)
        )
    )

    return query.all()
