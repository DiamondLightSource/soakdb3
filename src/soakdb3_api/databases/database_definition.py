import logging

# Base class for all aiosqlite database objects.
from soakdb3_api.databases.table_definitions import BodyTable, HeadTable, VisitTable

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class DatabaseDefinition:
    """
    Class which defines the database tables and revision migration path.
    Used in concert with the normsql class.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self):
        """
        Construct object.  Do not connect to database.
        """

        self.LATEST_REVISION = 1

    # ----------------------------------------------------------------------------------------
    async def add_table_definitions(self, database):
        """
        Make all the table definitions.
        """

        # Table schemas in our database.
        database.add_table_definition(HeadTable())
        database.add_table_definition(BodyTable())
        database.add_table_definition(VisitTable())

    # ----------------------------------------------------------------------------------------
    async def apply_revision(self, database, revision):

        # Let the base class add any common updates.
        # Usually only does anything if upgrading to revision 1
        # which means we are starting with a legacy database with no revision information.
        await NormsqlAiosqlite.apply_revision(self, database, revision)

        # Updating to revision 1 presumably means
        # this is a legacy database with no revision table in it.
        if revision == 1:
            await database.create_table(Tablenames.VISIT)

        # if revision == 2:
        #     await self.execute(
        #         f"ALTER TABLE {Tablenames.ROCKMAKER_IMAGES} ADD COLUMN {ImageFieldnames.NEWFIELD} TEXT",
        #         why=f"revision 2: add {Tablenames.ROCKMAKER_IMAGES} {ImageFieldnames.NEWFIELD} column",
        #     )
        #     await self.execute(
        #         "CREATE INDEX %s_%s ON %s(%s)"
        #         % (
        #             Tablenames.ROCKMAKER_IMAGES,
        #             ImageFieldnames.NEWFIELD,
        #             Tablenames.ROCKMAKER_IMAGES,
        #             ImageFieldnames.NEWFIELD,
        #         )
        #     )
