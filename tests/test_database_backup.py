import logging

from dls_normsql.databases import Databases

from soakdb3_api.databases.constants import BodyFieldnames, Tablenames
from soakdb3_api.databases.database_definition import DatabaseDefinition
from tests.base_tester import BaseTester2

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatabaseSqliteBackupRestore:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": "dls_normsql.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterBackupRestore().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class DatabaseTesterBackupRestore(BaseTester2):
    """
    Test direct SQL backup and restore.
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

        # Connect to database.
        await database.connect(should_drop_database=True)

        try:
            uuid1 = 1000
            uuid2 = 2000

            # Write one record.
            await database.insert(
                Tablenames.BODY,
                [{BodyFieldnames.LabVisit: "x", BodyFieldnames.ID: uuid1}],
            )

            # Backup.
            await database.backup()

            # Write another record.
            await database.insert(
                Tablenames.BODY,
                [{BodyFieldnames.LabVisit: "y", BodyFieldnames.ID: uuid2}],
            )

            # Backup again (with two records)
            await database.backup()

            # Restore one in the past (when it had a single record).
            await database.restore(1)

            all_sql = (
                f"SELECT * FROM {Tablenames.BODY} ORDER BY ID ASC /* first query */"
            )
            records = await database.query(all_sql)
            assert len(records) == 1, "first %s count expected 1" % (all_sql)

            # Restore most recent (two records).
            await database.restore(0)

            all_sql = f"SELECT * FROM {Tablenames.BODY} ORDER BY ID ASC"
            records = await database.query(all_sql)
            assert len(records) == 2, "second %s count expected 2" % (all_sql)

        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()
