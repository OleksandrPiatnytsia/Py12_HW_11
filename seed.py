from random import randint, choice

from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from db import session
from models import Teacher, Student, Group, Point, Subject

MIN_POINTS_COUNT = 7
MAX_POINTS_COUNT = 20

TEACHERS_COUNT = 5

STUDENTS_COUNT = 50

SUBJECTS = [
    "Математичний аналіз",
    "Історія",
    "Алхімія",
    "Загальна алгебра",
    "Квантова механіка",
    "Чисельні методи",
    "Теорія імовірності"
]

GROUPS = ["group 1", "group 2", "group 3"]

fake = Faker('uk-UA')


def generate_random_workday():
    random_day = datetime(datetime.now().year, 1, 1) + timedelta(
        days=randint(1, datetime.now().timetuple().tm_yday)
    )

    # Перевірка, чи день не вихідний
    while random_day.weekday() >= 5:
        random_day += timedelta(days=1)

    random_time = timedelta(hours=randint(8, 17), minutes=randint(0, 59))
    random_datetime = random_day + random_time

    # Перетворення на формат TIMESTAMP
    formatted_datetime = random_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def insert_data_to_DB():
    # insert data
    # TEACHERS
    if not session.query(Teacher).first():
        for i in range(1, TEACHERS_COUNT + 1):
            teacher = Teacher(name=fake.name())
            session.add(teacher)

    # GROUPS
    if not session.query(Group).first():
        for group_name in GROUPS:
            group = Group(name=group_name)
            session.add(group)

    # SUBJECTS
    if not session.query(Subject).first():
        for subject_name in SUBJECTS:
            tchr_list = session.query(Teacher).all()

            subject = Subject(name=subject_name, teacher_id=choice(tchr_list).id)
            session.add(subject)


    # STUDENTS
    if not session.query(Student).first():
        for _ in range(STUDENTS_COUNT):
            group_list = session.query(Group).all()

            student = Student(name=fake.name(), group_id=choice(group_list).id)
            session.add(student)


    # POINTS
    if not session.query(Point).first():
        students_list = session.query(Student).all()

        subj_list = session.query(Subject).all()

        for student in students_list:
            for _ in range(1, randint(MIN_POINTS_COUNT, MAX_POINTS_COUNT)):
                point = Point(student_id=student.id, subject_id=choice(subj_list).id, point=randint(1, 100),
                              created_at=generate_random_workday())
                session.add(point)


if __name__ == '__main__':
    try:
        insert_data_to_DB()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
