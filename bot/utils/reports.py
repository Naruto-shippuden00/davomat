"""Hisobot generatsiyasi"""
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date
from bot.models import Attendance, Student, Class, Subject
from config import EMOJI_TROPHY, EMOJI_WARNING, EMOJI_PRESENT, EMOJI_ABSENT, EMOJI_LATE

async def generate_daily_report(
    session: AsyncSession,
    class_id: int,
    report_date: date = None
) -> str:
    """Kunlik hisobot yaratish"""
    if report_date is None:
        report_date = date.today()
    
    # Sinfni olish
    class_obj = await session.get(Class, class_id)
    if not class_obj:
        return "❌ Sinf topilmadi"
    
    # O'quvchilar soni
    total_students_result = await session.execute(
        select(func.count(Student.id)).where(
            Student.class_id == class_id,
            Student.is_active == True
        )
    )
    total_students = total_students_result.scalar()
    
    # Bugungi davomat
    attendances_result = await session.execute(
        select(Attendance).where(
            Attendance.class_id == class_id,
            Attendance.date == report_date
        )
    )
    attendances = attendances_result.scalars().all()
    
    # Statistika
    present_count = len([a for a in attendances if a.status == "keldi"])
    absent_count = len([a for a in attendances if a.status == "kelmadi"])
    late_count = len([a for a in attendances if a.status == "kechikdi"])
    
    present_percent = (present_count / total_students * 100) if total_students > 0 else 0
    absent_percent = (absent_count / total_students * 100) if total_students > 0 else 0
    late_percent = (late_count / total_students * 100) if total_students > 0 else 0
    
    report = f"""
📅 Kunlik davomat hisoboti
📚 Sinf: {class_obj.name}
📆 Sana: {report_date.strftime("%d.%m.%Y")}

📊 STATISTIKA:
━━━━━━━━━━━━━━━━━━━━
👥 Jami o'quvchilar: {total_students}
{EMOJI_PRESENT} Kelganlar: {present_count} ({present_percent:.1f}%)
{EMOJI_ABSENT} Kelmaganlar: {absent_count} ({absent_percent:.1f}%)
{EMOJI_LATE} Kechikkanlar: {late_count} ({late_percent:.1f}%)
"""
    
    # Kelmaganlar ro'yxati
    if absent_count > 0:
        report += "\n❌ KELMAGANLAR:\n"
        for attendance in attendances:
            if attendance.status == "kelmadi":
                student = await session.get(Student, attendance.student_id)
                report += f"  • {student.full_name}\n"
    
    # Kechikkanlar ro'yxati
    if late_count > 0:
        report += "\n⏰ KECHIKKANLAR:\n"
        for attendance in attendances:
            if attendance.status == "kechikdi":
                student = await session.get(Student, attendance.student_id)
                minutes = attendance.late_minutes or 0
                report += f"  • {student.full_name} ({minutes} daq.)\n"
    
    return report

async def generate_weekly_report(
    session: AsyncSession,
    class_id: int,
    start_date: date = None
) -> str:
    """Haftalik hisobot yaratish"""
    if start_date is None:
        start_date = date.today() - timedelta(days=date.today().weekday())
    
    end_date = start_date + timedelta(days=6)
    
    # Sinfni olish
    class_obj = await session.get(Class, class_id)
    if not class_obj:
        return "❌ Sinf topilmadi"
    
    # O'quvchilar
    students_result = await session.execute(
        select(Student).where(
            Student.class_id == class_id,
            Student.is_active == True
        )
    )
    students = students_result.scalars().all()
    total_students = len(students)
    
    # Haftalik davomat
    attendances_result = await session.execute(
        select(Attendance).where(
            and_(
                Attendance.class_id == class_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        )
    )
    attendances = attendances_result.scalars().all()
    
    # Statistika
    present_count = len([a for a in attendances if a.status == "keldi"])
    absent_count = len([a for a in attendances if a.status == "kelmadi"])
    late_count = len([a for a in attendances if a.status == "kechikdi"])
    total_records = len(attendances)
    
    present_percent = (present_count / total_records * 100) if total_records > 0 else 0
    absent_percent = (absent_count / total_records * 100) if total_records > 0 else 0
    late_percent = (late_count / total_records * 100) if total_records > 0 else 0
    
    report = f"""
📊 Haftalik davomat hisoboti
📚 Sinf: {class_obj.name}
📆 Davr: {start_date.strftime("%d.%m.%Y")} - {end_date.strftime("%d.%m.%Y")}

📈 STATISTIKA:
━━━━━━━━━━━━━━━━━━━━
👥 Jami o'quvchilar: {total_students}
📝 Jami yozuvlar: {total_records}
{EMOJI_PRESENT} Kelganlar: {present_count} ({present_percent:.1f}%)
{EMOJI_ABSENT} Kelmaganlar: {absent_count} ({absent_percent:.1f}%)
{EMOJI_LATE} Kechikkanlar: {late_count} ({late_percent:.1f}%)
"""
    
    # Eng yaxshi qatnashgan o'quvchilar
    student_stats = {}
    for student in students:
        student_attendances = [a for a in attendances if a.student_id == student.id]
        present = len([a for a in student_attendances if a.status == "keldi"])
        total = len(student_attendances)
        if total > 0:
            student_stats[student] = (present, total, present / total * 100)
    
    if student_stats:
        top_students = sorted(student_stats.items(), key=lambda x: x[1][2], reverse=True)[:3]
        report += f"\n{EMOJI_TROPHY} ENG YAXSHI QATNASHGANLAR:\n"
        for i, (student, (present, total, percent)) in enumerate(top_students, 1):
            report += f"  {i}. {student.full_name}: {present}/{total} ({percent:.1f}%)\n"
        
        # Eng ko'p qolib ketganlar
        worst_students = sorted(student_stats.items(), key=lambda x: x[1][2])[:3]
        report += f"\n{EMOJI_WARNING} ENG KO'P QOLIB KETGANLAR:\n"
        for i, (student, (present, total, percent)) in enumerate(worst_students, 1):
            absent_percent = 100 - percent
            report += f"  {i}. {student.full_name}: {total - present}/{total} ({absent_percent:.1f}%)\n"
    
    return report

async def generate_monthly_report(
    session: AsyncSession,
    class_id: int,
    year: int = None,
    month: int = None
) -> str:
    """Oylik hisobot yaratish"""
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    # Sinfni olish
    class_obj = await session.get(Class, class_id)
    if not class_obj:
        return "❌ Sinf topilmadi"
    
    # O'quvchilar
    students_result = await session.execute(
        select(Student).where(
            Student.class_id == class_id,
            Student.is_active == True
        )
    )
    students = students_result.scalars().all()
    total_students = len(students)
    
    # Oylik davomat
    attendances_result = await session.execute(
        select(Attendance).where(
            and_(
                Attendance.class_id == class_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        )
    )
    attendances = attendances_result.scalars().all()
    
    # Statistika
    present_count = len([a for a in attendances if a.status == "keldi"])
    absent_count = len([a for a in attendances if a.status == "kelmadi"])
    late_count = len([a for a in attendances if a.status == "kechikdi"])
    total_records = len(attendances)
    
    present_percent = (present_count / total_records * 100) if total_records > 0 else 0
    absent_percent = (absent_count / total_records * 100) if total_records > 0 else 0
    late_percent = (late_count / total_records * 100) if total_records > 0 else 0
    
    month_names = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
    ]
    
    report = f"""
📈 Oylik davomat hisoboti
📚 Sinf: {class_obj.name}
📆 Oy: {month_names[month - 1]} {year}

📊 STATISTIKA:
━━━━━━━━━━━━━━━━━━━━
👥 Jami o'quvchilar: {total_students}
📝 Jami yozuvlar: {total_records}
{EMOJI_PRESENT} Kelganlar: {present_count} ({present_percent:.1f}%)
{EMOJI_ABSENT} Kelmaganlar: {absent_count} ({absent_percent:.1f}%)
{EMOJI_LATE} Kechikkanlar: {late_count} ({late_percent:.1f}%)

📋 O'QUVCHILAR BO'YICHA TAHLIL:
━━━━━━━━━━━━━━━━━━━━
"""
    
    # Har bir o'quvchi uchun statistika
    for student in students:
        student_attendances = [a for a in attendances if a.student_id == student.id]
        present = len([a for a in student_attendances if a.status == "keldi"])
        absent = len([a for a in student_attendances if a.status == "kelmadi"])
        late = len([a for a in student_attendances if a.status == "kechikdi"])
        total = len(student_attendances)
        
        if total > 0:
            percent = present / total * 100
            report += f"\n{student.full_name}:\n"
            report += f"  {EMOJI_PRESENT} Keldi: {present}, {EMOJI_ABSENT} Kelmadi: {absent}, {EMOJI_LATE} Kechikdi: {late}\n"
            report += f"  Davomat: {percent:.1f}%\n"
    
    return report
