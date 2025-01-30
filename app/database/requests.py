from app.database.models import async_session
from app.database.models import Version
from sqlalchemy import select

async def save_version_in_db(version):
    async with async_session() as session:
        search_version_in_db = await session.scalar(select(Version).where(Version.version == version))
        
        if search_version_in_db:
            print(f'[+]...Версия {version} уже есть в базе...')
        
        else:
            session.add(Version(version=version))
            print(f'[+]...Версия {version} сохранена...')
            await session.commit()

    
async def get_last_version_from_db():
    async with async_session() as session:
        return await session.scalar(select(Version).order_by(Version.create_data.desc()))

