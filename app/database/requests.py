from app.database.models import async_session
from app.database.models import Version
from sqlalchemy import select

async def save_version_in_db(version):
    async with async_session() as session:
        version = await session.scalar(select(Version).where(Version.version == version))
        
        if version:
            print(f'[+]...Версия {version} уже есть в базе...')
        elif version is None:
            print(f'[+]...Версия {version}...')
        else:
            session.add(Version(version=version))
            print(f'[+]...Версия {version} сохранена...')
            await session.commit()

