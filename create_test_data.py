"""Railway uchun test ma'lumotlarini yaratish"""
import asyncio
from datetime import date
from bot.models import get_session, User, Class, Student, Subject
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_PARENT, ADMIN_TELEGRAM_ID

async def create_test_data():
    """Test ma'lumotlarini yaratish"""
    print("Test ma'lumotlarini qo'shish...")
    
    async for session in get_session():
        # Sinflar
        class_9a = Class(
            name="9-A",
            grade=9,
            section="A",
            academic_year="2023-2024"
        )
        session.add(class_9a)
        
        class_10b = Class(
            name="10-B",
            grade=10,
            section="B",
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
        ]
        
        for subject in subjects:
            session.add(subject)
        
        await session.commit()
        
        # O'quvchilar - 9-A sinf
        students = [
            Student(
                full_name="Alisher Umarov",
                class_id=class_9a.id,
                date_of_birth=date(2009, 3, 15),
                gender="erkak"
            ),
            Student(
                full_name="Dilnoza Rahimova",
                class_id=class_9a.id,
                date_of_birth=date(2009, 5, 20),
                gender="ayol"
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
        ]
        
        for student in students:
            session.add(student)
        
        await session.commit()
        
        print("✅ Test ma'lumotlari muvaffaqiyatli yaratildi!")
        print(f"\n📚 Sinflar: {len([class_9a, class_10b])}")
        print(f"📖 Fanlar: {len(subjects)}")
        print(f"👥 O'quvchilar: {len(students)}")
        break

if __name__ == "__main__":
    asyncio.run(create_test_data())
