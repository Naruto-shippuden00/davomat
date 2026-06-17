"""Test ma'lumotlarini yaratish"""
import asyncio
from datetime import date
from bot.models import Base, init_db, get_session, User, Class, Student, Subject
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_PARENT

async def create_sample_data():
    """Test ma'lumotlarini yaratish"""
    print("Ma'lumotlar bazasini tozalash va qayta yaratish...")
    await init_db()
    
    async for session in get_session():
        print("Test ma'lumotlarini qo'shish...")
        
        # Admin foydalanuvchi
        admin = User(
            telegram_id=123456789,  # Bu yerga haqiqiy telegram ID kiriting
            username="admin",
            full_name="Admin Adminov",
            phone="+998901234567",
            role=ROLE_ADMIN
        )
        session.add(admin)
        
        # Sinf rahbari
        class_teacher = User(
            telegram_id=987654321,  # Bu yerga haqiqiy telegram ID kiriting
            username="teacher1",
            full_name="Aziza Karimova",
            phone="+998901234568",
            role=ROLE_CLASS_TEACHER
        )
        session.add(class_teacher)
        
        # O'qituvchi
        teacher = User(
            telegram_id=111222333,  # Bu yerga haqiqiy telegram ID kiriting
            username="teacher2",
            full_name="Javohir Rahimov",
            phone="+998901234569",
            role=ROLE_TEACHER
        )
        session.add(teacher)
        
        # Ota-onalar
        parent1 = User(
            telegram_id=444555666,  # Bu yerga haqiqiy telegram ID kiriting
            username="parent1",
            full_name="Dilshod Yusupov",
            phone="+998901234570",
            role=ROLE_PARENT
        )
        session.add(parent1)
        
        parent2 = User(
            telegram_id=777888999,  # Bu yerga haqiqiy telegram ID kiriting
            username="parent2",
            full_name="Malika Tosheva",
            phone="+998901234571",
            role=ROLE_PARENT
        )
        session.add(parent2)
        
        await session.commit()
        
        # Sinflar
        class_9a = Class(
            name="9-A",
            grade=9,
            section="A",
            class_teacher_id=class_teacher.id,
            academic_year="2023-2024"
        )
        session.add(class_9a)
        
        class_10b = Class(
            name="10-B",
            grade=10,
            section="B",
            class_teacher_id=class_teacher.id,
            academic_year="2023-2024"
        )
        session.add(class_10b)
        
        await session.commit()
        
        # Fanlar
        subjects = [
            Subject(name="Matematika", code="MAT"),
            Subject(name="Fizika", code="FIZ"),
            Subject(name="Ona tili", code="ONA"),
            Subject(name="Ingliz tili", code="ING"),
            Subject(name="Kimyo", code="KIM"),
            Subject(name="Biologiya", code="BIO"),
            Subject(name="Tarix", code="TAR"),
            Subject(name="Informatika", code="INF")
        ]
        
        for subject in subjects:
            session.add(subject)
        
        await session.commit()
        
        # O'quvchilar - 9-A sinf
        students_9a = [
            Student(
                full_name="Alisher Umarov",
                class_id=class_9a.id,
                parent_id=parent1.id,
                date_of_birth=date(2009, 3, 15),
                gender="erkak",
                parent_phone="+998901234570"
            ),
            Student(
                full_name="Dilnoza Rahimova",
                class_id=class_9a.id,
                parent_id=parent2.id,
                date_of_birth=date(2009, 5, 20),
                gender="ayol",
                parent_phone="+998901234571"
            ),
            Student(
                full_name="Sardor Karimov",
                class_id=class_9a.id,
                date_of_birth=date(2009, 1, 10),
                gender="erkak"
            ),
            Student(
                full_name="Madina Tosheva",
                class_id=class_9a.id,
                date_of_birth=date(2009, 8, 25),
                gender="ayol"
            ),
            Student(
                full_name="Bobur Aliyev",
                class_id=class_9a.id,
                date_of_birth=date(2009, 11, 5),
                gender="erkak"
            ),
            Student(
                full_name="Zilola Hasanova",
                class_id=class_9a.id,
                date_of_birth=date(2009, 4, 18),
                gender="ayol"
            ),
            Student(
                full_name="Jasur Yusupov",
                class_id=class_9a.id,
                date_of_birth=date(2009, 7, 30),
                gender="erkak"
            ),
            Student(
                full_name="Nigora Azizova",
                class_id=class_9a.id,
                date_of_birth=date(2009, 2, 12),
                gender="ayol"
            )
        ]
        
        for student in students_9a:
            session.add(student)
        
        # O'quvchilar - 10-B sinf
        students_10b = [
            Student(
                full_name="Jahongir Mahmudov",
                class_id=class_10b.id,
                date_of_birth=date(2008, 6, 8),
                gender="erkak"
            ),
            Student(
                full_name="Feruza Sabirova",
                class_id=class_10b.id,
                date_of_birth=date(2008, 9, 22),
                gender="ayol"
            ),
            Student(
                full_name="Aziz Normatov",
                class_id=class_10b.id,
                date_of_birth=date(2008, 3, 14),
                gender="erkak"
            ),
            Student(
                full_name="Laylo Karimova",
                class_id=class_10b.id,
                date_of_birth=date(2008, 12, 1),
                gender="ayol"
            ),
            Student(
                full_name="Timur Rashidov",
                class_id=class_10b.id,
                date_of_birth=date(2008, 5, 28),
                gender="erkak"
            )
        ]
        
        for student in students_10b:
            session.add(student)
        
        await session.commit()
        
        print("✅ Test ma'lumotlari muvaffaqiyatli yaratildi!")
        print("\n📝 Test foydalanuvchilar:")
        print(f"Admin: telegram_id={admin.telegram_id}")
        print(f"Sinf rahbari: telegram_id={class_teacher.telegram_id}")
        print(f"O'qituvchi: telegram_id={teacher.telegram_id}")
        print(f"Ota-ona 1: telegram_id={parent1.telegram_id}")
        print(f"Ota-ona 2: telegram_id={parent2.telegram_id}")
        print("\n⚠️ MUHIM: Bu telegram ID larni o'z telegram ID laringizga o'zgartiring!")

if __name__ == "__main__":
    asyncio.run(create_sample_data())
