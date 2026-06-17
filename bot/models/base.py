"""Ma'lumotlar bazasi asosiy sozlamalari"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL

# Base class
class Base(DeclarativeBase):
    pass

# Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Ma'lumotlar bazasini yaratish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Sessiya yaratish"""
    async with async_session_maker() as session:
        yield session
