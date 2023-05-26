import logging

from dls_normsql.constants import ClassTypes
from dls_normsql.databases import Databases

from soakdb3_api.databases.constants import BodyFieldnames, HeadFieldnames, Tablenames
from soakdb3_api.databases.database_definition import DatabaseDefinition
from tests.base_tester import BaseTester2

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatabaseHead:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": ClassTypes.AIOSQLITE,
            "filename": "%s/soakdb3_pytest.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterHead().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class TestDatabaseBody:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": "dls_normsql.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterBody().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class DatabaseTesterHead(BaseTester2):
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

        # Connect to database.
        await database.connect(should_drop_database=True)

        try:
            # Write one record.
            await database.insert(
                Tablenames.HEAD,
                [{HeadFieldnames.LabVisit: "x", HeadFieldnames.Protein: "y"}],
            )

            all_sql = "SELECT * FROM soakDB"
            records = await database.query(all_sql)
            assert len(records) == 1
        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()


# ----------------------------------------------------------------------------------------
class DatabaseTesterBody(BaseTester2):
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

            uuid1 = 1000
            uuid2 = 2000
            uuid3 = 3000

            # Write one record.
            await database.insert(
                Tablenames.BODY,
                [{BodyFieldnames.LabVisit: "x", BodyFieldnames.ID: uuid1}],
            )
            all_sql = f"SELECT * FROM {Tablenames.BODY} ORDER BY ID ASC"
            records = await database.query(all_sql)
            assert len(records) == 1, "first %s count" % (all_sql)

            # Write two more records.
            await database.insert(
                Tablenames.BODY,
                [
                    {BodyFieldnames.LabVisit: "y", BodyFieldnames.ID: uuid2},
                    {BodyFieldnames.LabVisit: "z", BodyFieldnames.ID: uuid3},
                ],
            )
            records = await database.query(all_sql)
            assert len(records) == 3, "second %s count" % (all_sql)

            # Update one record to BUSY.
            await database.update(
                Tablenames.BODY, {BodyFieldnames.LabVisit: "z2"}, f"ID = {uuid3}"
            )
            z2_sql = f"SELECT * FROM {Tablenames.BODY} WHERE {BodyFieldnames.LabVisit} = 'z2' ORDER BY ID ASC"
            records = await database.query(z2_sql)
            assert len(records) == 1, "%s count" % z2_sql

            # Update two records to DEAD.
            await database.update(
                Tablenames.BODY,
                {BodyFieldnames.LabVisit: "u2"},
                f"ID IN ({uuid1}, {uuid2})",
            )
            u2_sql = f"SELECT * FROM {Tablenames.BODY} WHERE {BodyFieldnames.LabVisit} = 'u2' ORDER BY ID ASC"
            records = await database.query(u2_sql)
            assert len(records) == 2, "%s count" % u2_sql

        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()
