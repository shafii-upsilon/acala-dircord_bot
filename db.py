from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://acala.sqlite3',
        modules={'models': ['models']}
    )
    
    # await Tortoise.generate_schemas()
