from fastorm import FastORM

DATABASE_URL = 'postgresql://postgres:AA188601@localhost:5432/fast-orm-user-and-employee'

async def get_db_connection():
    return await FastORM.create_connection(DATABASE_URL)
