from datetime import datetime

from sqlalchemy import text

from src.database.models import Contact


def get_contacts(session):
    contacts = session.query(Contact).all()
    return contacts


def get_contact_by_id(contact_id, session):
    contact = session.query(Contact).filter_by(id=contact_id).first()

    return contact

def get_contact_by_phone(phone, session):

    return session.query(Contact).filter_by(phone=phone).first()


def get_contact_by_name(name, session):
    return session.query(Contact).filter_by(name=name).first()



def get_contact_by_email(email, session):
    return session.query(Contact).filter_by(email=email).first()



def get_contact_by_sur_name(sur_name, session):
    return session.query(Contact).filter_by(sur_name=sur_name).first()



def create_contact(body, session):

    contact = Contact()
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    session.add(contact)
    session.commit()
    return contact


def delete_contact(contact, session):
    session.delete(contact)
    session.commit()

    return contact


def update_contact(body, contact, session):
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    session.add(contact)
    session.commit()

    return contact


def get_contact_week_birthdays(session):
    current_date = datetime.now()
    current_month = current_date.month

    contacts = session.execute(text("""
            SELECT *
            FROM contacts AS con
            WHERE EXTRACT(WEEK FROM con.birthday) = EXTRACT(WEEK FROM :current_date)
              AND EXTRACT(MONTH FROM con.birthday) = :current_month;
            """), {"current_date": current_date, "current_month": current_month}).all()

    return contacts
