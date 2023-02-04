import asyncio
import logging
import multiprocessing

import pytest

from soakdb3_api.databases.constants import BodyFieldnames, HeadFieldnames, Tablenames
from soakdb3_lib.databases.databases import Databases

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatabaseHead:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": "soakdb3_lib.databases.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
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
            "type": "soakdb3_lib.databases.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterBody().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class TestDatabaseSqliteBackupRestore:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of XchemBeDatabase.
        """

        database_specification = {
            "type": "soakdb3_lib.databases.aiosqlite",
            "filename": "%s/soakdb3.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterBackupRestore().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class _BaseTester:
    """
    Provide asyncio loop and error checking over *Tester classes.
    """

    def main(self, constants, specification, output_directory):
        """
        This is the main program which calls the test using asyncio.
        """

        multiprocessing.current_process().name = "main"

        failure_message = None
        try:
            # Run main test in asyncio event loop.
            asyncio.run(
                self._main_coroutine(constants, specification, output_directory)
            )

        except Exception as exception:
            logger.exception(
                "unexpected exception in the test method", exc_info=exception
            )
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)


# ----------------------------------------------------------------------------------------
class DatabaseTesterHead(_BaseTester):
    """
    Test direct SQL access to the database.
    """

    async def _main_coroutine(
        self, constants, database_specification, output_directory
    ):
        """ """

        databases = Databases()
        database = databases.build_object(database_specification)

        # Connect to database.
        await database.connect()

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
class DatabaseTesterBody(_BaseTester):
    """
    Test direct SQL access to the database.
    """

    async def _main_coroutine(
        self, constants, database_specification, output_directory
    ):
        """ """

        databases = Databases()
        database = databases.build_object(database_specification)

        try:
            # Connect to database.
            await database.connect()

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


# ----------------------------------------------------------------------------------------
class DatabaseTesterBackupRestore(_BaseTester):
    """
    Test direct SQL backup and restore.
    """

    async def _main_coroutine(
        self, constants, database_specification, output_directory
    ):
        """ """

        databases = Databases()
        database = databases.build_object(database_specification)

        # Connect to database.
        await database.connect()

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
