import logging

# Base class for the aiosqlite database object.
from dls_normsql.aiosqlite import Aiosqlite as NormsqlAiosqlite

from soakdb3_api.databases.constants import Tablenames

# Base class for our database definition.
from soakdb3_lib.databases.database_definition import DatabaseDefinition

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class Aiosqlite(DatabaseDefinition, NormsqlAiosqlite):
    """
    Class with coroutines for creating and querying a sqlite database.
    We use dls-normsql to do the heavy lifting.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):
        """
        Construct object.  Do not connect to database.
        """

        # Constructor for the database definition.
        DatabaseDefinition.__init__(self)

        # Constructor for the database implementation.
        NormsqlAiosqlite.__init__(self, specification)

    # ----------------------------------------------------------------------------------------
    def reinstance(self):
        """
        Clone database instance.
        This is needed if a process inherits an instance, but needs its own connection.
        """

        return Aiosqlite(self.__filename)

    # ----------------------------------------------------------------------------------------
    async def add_table_definitions(self):
        """
        Make all the table definitions.
        """

        # Add tables common in all implementations.
        await NormsqlAiosqlite.add_table_definitions(self)

        # Add tables from our definition.
        await DatabaseDefinition.add_table_definitions(self)

    # ----------------------------------------------------------------------------------------
    async def apply_revision(self, revision):

        # Let the base class add any common updates.
        # Usually only does anything if upgrading to revision 1
        # which means we are starting with a legacy database with no revision information.
        await NormsqlAiosqlite.apply_revision(self, revision)

        # Updating to revision 1 presumably means
        # this is a legacy database with no revision table in it.
        if revision == 1:
            await self.create_table(Tablenames.VISIT)

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
