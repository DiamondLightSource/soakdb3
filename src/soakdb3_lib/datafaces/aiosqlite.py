import copy
import csv
import logging
import os
import re

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.require import require

# Base class for generic things.
from dls_utilpack.thing import Thing

# Database constants.
from soakdb3_api.databases.constants import Tablenames

# Database manager.
from soakdb3_lib.databases.databases import Databases

# Version for health response.
from soakdb3_lib.version import version as soakdb3_lib_version

logger = logging.getLogger(__name__)

thing_type = "soakdb3_lib.datafaces.aiosqlite"


class Aiosqlite(Thing):
    """
    Implementation of dataface on top of underlying database API provider presumed to be sqlite.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):
        Thing.__init__(self, thing_type, specification)

        self.__type_specific = require(
            f"{callsign(self)} specification",
            self.specification(),
            "type_specific_tbd",
        )

        self.__dbspec = require(
            f"{callsign(self)} specification",
            self.__type_specific,
            "database",
        )

        self.__visitid_mappings = require(
            f"{callsign(self)} specification",
            self.__type_specific,
            "visitid_mappings",
        )

        # Cache of database objects we have created.
        self.__cache = {}
        self.__cache_cvs_directories = {}

    # ----------------------------------------------------------------------------------------
    async def start(self):
        # There is no visitid known at start of the server.
        # They are built up as requested by clients.

        pass

    # ----------------------------------------------------------------------------------------
    async def disconnect(self):
        visitids = list(self.__cache.keys())
        for visitid in visitids:
            database = self.__cache.pop(visitid)
            await database.disconnect()
            database = None

    # ----------------------------------------------------------------------------------------
    async def establish_database_connection(self, visitid):

        database = self.__cache.get(visitid)
        if database is None:

            # Get path from visitid.
            visitid_path = self.__visitid2path(visitid)

            logger.debug(f"visitid {visitid} is for path {visitid_path}")

            if not os.path.isdir(visitid_path):
                raise RuntimeError(f"{visitid_path} is not a directory")

            # Get copy of specification template.
            dbspec = copy.deepcopy(self.__dbspec)

            dbspec["filename"] = f"{visitid_path}/database/soakDBDataFile.sqlite"
            dbspec["backup_directory"] = f"{visitid_path}/database/DataFileBackups"

            self.__cache_cvs_directories[visitid] = f"{visitid_path}/lab36"

            database = Databases().build_object(dbspec)
            await database.connect()

            # Cache database connections by visitid.
            self.__cache[visitid] = database

        return database

    # ----------------------------------------------------------------------------------------
    def __visitid2path(self, visitid: str) -> str:
        """
        Give back a file path given the visitid.

        Args:
            visitid (str): visitid
                At the current time, excel gives the visitid as windows-type path with leading drive letter.

        Returns:
            str: Linux filesystem path root of the database, backup and csv files.

        """

        # Go through all the mappings defined in the specification.
        for visitid_mapping in self.__visitid_mappings:
            # This mapping calls for regex replacement?
            if visitid_mapping["action"] == "regex_replace":
                pattern = visitid_mapping["pattern"]
                replace = visitid_mapping["replace"]

                # The visitid matches this mapping?
                match = re.search(pattern, visitid)
                if match is not None:
                    # Replace with the substitution.
                    path = re.sub(pattern, replace, visitid)
                    return path

        return visitid

    # # ----------------------------------------------------------------------------------------
    # async def reinstance(self):
    #     """"""

    #     # TODO: Consider if reinstance is a necessary method.
    #     if self.__database is None:
    #         return

    #     self.__database = self.__database.reinstance()

    # ----------------------------------------------------------------------------------------
    async def backup(self, visitid):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.backup()

    # ----------------------------------------------------------------------------------------
    async def restore(self, visitid, nth):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.restore(nth)

    # ----------------------------------------------------------------------------------------
    async def query_for_dictionary(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        records = await database.query(sql, subs=subs, why=why)

        return records

    # ----------------------------------------------------------------------------------------
    async def query(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        records = await database.query(sql, subs=subs, why=why)

        # Make a VBA collection with the first record giving the field names.
        collection = []
        for index, record in enumerate(records):
            if index == 0:
                collection.append(list(record.keys()))
            collection.append(list(record.values()))

        return collection

    # ----------------------------------------------------------------------------------------
    async def execute(self, visitid, sql, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        return await database.execute(sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def insert(self, visitid, table_name, records, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        if why is None:
            why = f"insert {len(records)} {table_name} records"

        await database.insert(table_name, records)

    # ----------------------------------------------------------------------------------------
    async def update(self, visitid, table_name, record, where, subs=None, why=None):
        """"""
        database = await self.establish_database_connection(visitid)

        if why is None:
            why = f"update {table_name} record"

        await database.update(table_name, record, where, why=why)

    # ----------------------------------------------------------------------------------------
    async def update_body_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """
        database = await self.establish_database_connection(visitid)

        table_name = Tablenames.BODY

        maximum_id = None
        # Group the updates to rows by their id.
        rows = {}
        new_ids = {}
        for field in fields:
            id = str(field["id"])
            # This is a new row created from within the client?
            if id[0] == "-":
                # We haven't assigned this record to a real database id yet?
                if id not in new_ids:
                    # We don't know the maximum id in the database yet?
                    if maximum_id is None:
                        maximum_id = await self.query_for_dictionary(
                            visitid, f"SELECT MAX(ID) AS MAX_ID FROM {table_name}"
                        )
                        maximum_id = maximum_id[0]["MAX_ID"]
                    if maximum_id is None:
                        maximum_id = 0
                    maximum_id += 1
                    new_ids[id] = str(maximum_id)
                # Translate the negative id to a new id in the database.
                id = new_ids[id]

            row = rows.get(id)
            if row is None:
                row = []
                rows[id] = row

            # VBA doesn't put a Nothing value in the dictionary, so treat missing value as None.
            value = field.get("value")
            row.append({"field": field["field"], "value": value})

        # Get list of existing ids for those we want to update.
        id_csv = ", ".join(rows.keys())
        existing_rows = await self.query_for_dictionary(
            visitid, f"SELECT ID FROM {table_name} WHERE ID IN ({id_csv})"
        )
        existing_ids = []
        for existing_row in existing_rows:
            existing_ids.append(str(existing_row["ID"]))

        new_rows = []
        for updated_id in rows.keys():
            if updated_id not in existing_ids:
                new_rows.append({"ID": updated_id})

        logger.debug(
            f"inserting {len(new_rows)} new rows"
            f" and updating {len(rows.keys())} rows"
        )

        try:
            # Do the inserts at the start of the transaction.
            await database.insert(
                Tablenames.BODY,
                new_rows,
                should_commit=False,
            )

            # Perform the updates on each row.
            for id, row in rows.items():
                sets = []
                subs = []
                for k in row:
                    field = k["field"]
                    value = k["value"]
                    sets.append(f"`{field}` = ?")
                    subs.append(value)
                subs.append(id)

                sets = ", ".join(sets)
                sql = f"UPDATE {table_name} SET {sets} WHERE ID = ?"

                # Add the update to the transaction.
                await database.execute(
                    sql,
                    subs=subs,
                    should_commit=False,
                )
        except Exception:
            # Don't keep any partial operation.
            database.rollback()
            raise

        # Commit all the updates.
        logger.debug(
            f"committing {len(new_rows)} new rows"
            f" and updating {len(rows.keys())} rows"
        )
        await database.commit()
        logger.debug("committed")

    # ----------------------------------------------------------------------------------------
    async def update_head_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """

        table_name = Tablenames.HEAD

        # Perform the updates on the only row row.
        sets = []
        subs = []
        for k in fields:
            field = k["field"]
            value = k["value"]
            sets.append(f"`{field}` = ?")
            subs.append(value)

        sets = ", ".join(sets)
        sql = f"UPDATE {table_name} SET {sets}"

        await self.execute(visitid, sql, subs=subs, why="update head table")

    # ----------------------------------------------------------------------------------------
    async def write_csv(self, visitid, rows, filename):
        """
        Handle request to write rows as csv file.

        The rows are assumed fully prepared ahead of time.

        The filename's path should be a subdirectory (no leading slash).
        """

        # We don't really need the database itself, since all the data rows are provided as arguments.
        # However, this sets up the csv_directory for this visit.
        await self.establish_database_connection(visitid)

        # Get the csv directory from the specification.
        csv_directory = self.__cache_cvs_directories.get(visitid)
        if csv_directory is None:
            raise RuntimeError(
                f"no database connection has yet been made for visitid {visitid}"
            )

        filename = f"{csv_directory}/{filename}"
        await self.__create_directory(filename)

        with open(filename, "w") as stream:

            # Create the csv writer.
            writer = csv.writer(stream)

            # Write all rows to the csv file.
            writer.writerows(rows)

    # ----------------------------------------------------------------------------------------
    async def __create_directory(self, filename):

        directory, filename = os.path.split(filename)

        if not os.path.exists(directory):
            # Make sure that parent directories which get created will have public permission.
            umask = os.umask(0)
            os.umask(umask & ~0o0777)
            os.makedirs(directory)
            os.umask(umask)

    # ----------------------------------------------------------------------------------------
    async def report_health(self):
        """"""

        report = {}

        report["alive"] = True
        report["version"] = soakdb3_lib_version()

        return report

    # ----------------------------------------------------------------------------------------
    async def open_client_session(self):
        """"""
        # Connect to the database to create the schemas if they don't exist already.
        await self.establish_database_connection()

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""
        await self.disconnect()
