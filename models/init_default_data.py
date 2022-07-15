from models.tabs import Models, Manufactures, VinCodes


async def init_default_data(db_session):
    """
    Creates tables in the database and initializes the default values for the test
    """
    await db_session.create_all(Models)
    await db_session.create_all(Manufactures)
    await db_session.create_all(VinCodes)
    if not await Models.check_data(db_session):
        await Models.new_instance(db_session, "AMG GT roadster")
    if not await Manufactures.check_data(db_session):
        await Manufactures.new_instance(db_session, "Mercedes-Benz-Group")
    if not await VinCodes.check_data(db_session):
        await VinCodes.new_vin_code(session=db_session, name="4Y1SL65848Z411439", model_id=1, manufacture_id=1)
