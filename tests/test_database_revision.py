import logging

from dls_normsql.constants import Tablenames as DlsNormsqlTablenames
from dls_normsql.databases import Databases

from soakdb3_api.databases.constants import Tablenames
from soakdb3_api.databases.database_definition import DatabaseDefinition
from tests.base_tester import BaseTester2

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatabaseRevision:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": "dls_normsql.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterRevision().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class DatabaseTesterRevision(BaseTester2):
    """
    Test direct SQL access to the database.
    """

    async def _main_coroutine(
        self, constants, database_specification, output_directory
    ):
        """ """
        databases = Databases()
        database = databases.build_object(
            database_specification,
            DatabaseDefinition(),
        )

        try:
            # Connect to database.
            await database.connect(should_drop_database=True)

            sql = f"SELECT * FROM {DlsNormsqlTablenames.REVISION}"
            records = await database.query(sql)
            assert len(records) == 1

            sql = f"SELECT * FROM {Tablenames.VISIT}"
            records = await database.query(sql)
            assert len(records) == 0

            await database.execute(f"DROP TABLE {DlsNormsqlTablenames.REVISION}")
            await database.execute(f"DROP TABLE {Tablenames.VISIT}")

        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()

        try:
            # Connect to database, revision should be applied to add back the Visit and Revision tables.
            await database.connect()

            # Make sure we are up to date with the latest database schema revision.
            await database.apply_revisions()

            sql = f"SELECT * FROM {DlsNormsqlTablenames.REVISION}"
            records = await database.query(sql)
            assert len(records) == 1

            sql = f"SELECT * FROM {Tablenames.VISIT}"
            records = await database.query(sql)
            assert len(records) == 0

        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()
