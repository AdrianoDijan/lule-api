import asyncio

from gino.ext.starlette import Gino

from ...settings import DB_URL

db = Gino(dsn=DB_URL)


async def main():
    await db.set_bind(DB_URL)
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
