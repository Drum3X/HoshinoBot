
async def prepare_database(db):
    await db.execute("create table if not exists settings (maintenance int)")
    await db.execute("create table if not exists blacklist (ids int)")
    await db.commit()