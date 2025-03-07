from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем базу данных
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite')


# Создаем сессию
async_session = async_sessionmaker(engine)


# Базовый класс
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Таблица для записи версии
class Version(Base):
    __tablename__ = 'versions'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    create_data: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


# В асинхронном режиме запускаем сессию и создаем таблицы
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)