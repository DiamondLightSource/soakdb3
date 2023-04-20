import logging

import pytest

from soakdb3_api.databases.constants import BodyFieldnames, HeadFieldnames, Tablenames

# Client context creator.
from soakdb3_api.datafaces.context import Context as Soakdb3DatafaceClientContext
from soakdb3_api.datafaces.datafaces import datafaces_get_default

# Server context creator.
from soakdb3_lib.datafaces.context import Context as Soakdb3DatafaceServerContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatafaceHead:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/services.yaml"
        DatafaceHeadTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class TestDatafaceBody:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/services.yaml"
        DatafaceBodyTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class DatafaceHeadTester(BaseContextTester):
    """
    Class to test the news.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """

        multiconf = self.get_multiconf()

        multiconf_dict = await multiconf.load()

        # Reference the dict entry for the soakdb3 dataface.
        soakdb3_dataface_specification = multiconf_dict[
            "soakdb3_dataface_specification"
        ]

        # Make the server context.
        soakdb3_server_context = Soakdb3DatafaceServerContext(
            soakdb3_dataface_specification
        )

        # Make the client context.
        soakdb3_client_context = Soakdb3DatafaceClientContext(
            soakdb3_dataface_specification
        )

        # Start the soakdb3 server context which includes the direct or network-addressable service.
        async with soakdb3_server_context:
            # Start the matching soakdb3 client context.
            async with soakdb3_client_context:
                await self.__run_the_head_test(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_the_head_test(self, constants, output_directory):
        """ """

        # The visitid to match what is in the test configuration yaml.
        visitid = output_directory

        dataface = datafaces_get_default()

        # Write one record.
        await dataface.insert(
            visitid,
            Tablenames.HEAD,
            [
                {
                    HeadFieldnames.LabVisit: "x",
                    HeadFieldnames.Protein: "y",
                }
            ],
        )

        # --------------------------------------------------------------------
        # Update like XChem soakdb range changed.
        fields = [
            {"field": HeadFieldnames.LabVisit, "value": "a"},
            {"field": HeadFieldnames.Protein, "value": "b"},
            {"field": HeadFieldnames.DropVolume, "value": 1.23},
        ]

        await dataface.update_head_fields(visitid, fields)

        z3_sql = "SELECT * from soakDB"
        records = await dataface.query_for_dictionary(visitid, z3_sql)
        assert len(records) == 1
        assert records[0][HeadFieldnames.LabVisit] == "a"
        assert records[0][HeadFieldnames.Protein] == "b"
        assert records[0][HeadFieldnames.DropVolume] == 1.23

        # Query for invalid visit.
        with pytest.raises(RuntimeError) as exception_info:
            records = await dataface.query_for_dictionary("badvisit", z3_sql)
        assert "badvisit" in str(exception_info.value)


# ----------------------------------------------------------------------------------------
class DatafaceBodyTester(BaseContextTester):
    """
    Class to test the news.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """

        multiconf = self.get_multiconf()

        multiconf_dict = await multiconf.load()

        # Reference the dict entry for the soakdb3 dataface.
        soakdb3_dataface_specification = multiconf_dict[
            "soakdb3_dataface_specification"
        ]

        # Make the server context.
        soakdb3_server_context = Soakdb3DatafaceServerContext(
            soakdb3_dataface_specification
        )

        # Make the client context.
        soakdb3_client_context = Soakdb3DatafaceClientContext(
            soakdb3_dataface_specification
        )

        # Start the soakdb3 server context which includes the direct or network-addressable service.
        async with soakdb3_server_context:
            # Start the matching soakdb3 client context.
            async with soakdb3_client_context:
                await self.__run_the_body_test(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_the_body_test(self, constants, output_directory):
        """ """

        # The visitid to match what is in the test configuration yaml.
        visitid = output_directory

        uuid1 = 1000
        uuid2 = 2000
        uuid3 = 3000

        dataface = datafaces_get_default()

        # Write one record.
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.LabVisit: "x",
                    BodyFieldnames.ID: uuid1,
                }
            ],
        )

        all_sql = f"SELECT * FROM {Tablenames.BODY} ORDER BY ID ASC"
        records = await dataface.query(visitid, all_sql)
        assert len(records) == 2, "first %s count" % (all_sql)

        # Write two more records.
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.LabVisit: "y",
                    BodyFieldnames.ID: uuid2,
                },
                {
                    BodyFieldnames.LabVisit: "z",
                    BodyFieldnames.ID: uuid3,
                },
            ],
        )
        records = await dataface.query(visitid, all_sql)
        assert len(records) == 4, "second %s count" % (all_sql)

        # Update one record.
        await dataface.update(
            visitid,
            Tablenames.BODY,
            {BodyFieldnames.LabVisit: "z2"},
            f"ID = '{uuid3}'",
        )
        z2_sql = f"SELECT * FROM {Tablenames.BODY} WHERE {BodyFieldnames.LabVisit} = 'z2' ORDER BY ID ASC"
        records = await dataface.query(visitid, z2_sql)
        assert len(records) == 2, "third %s count" % z2_sql

        # --------------------------------------------------------------------
        # Update like XChem soakdb range changed.
        fields = [
            {"id": uuid1, "field": BodyFieldnames.CompoundCode, "value": 15},
            {"id": uuid2, "field": BodyFieldnames.CompoundCode, "value": 20},
            {"id": uuid3, "field": BodyFieldnames.CompoundCode, "value": 20},
        ]

        await dataface.update_body_fields(visitid, fields)

        z3_sql = (
            f"SELECT ID, {BodyFieldnames.CompoundCode} FROM mainTable ORDER BY ID ASC"
        )
        records = await dataface.query(visitid, z3_sql)
        assert len(records) == 4, "fourth %s count" % z3_sql
        assert records[1][1] == "15", "first compound"
        assert records[2][1] == "20", "second compound"
        assert records[3][1] == "20", "third compound"

        # # Update two records to DEAD.
        # await database.xchem_be_body_table.update(
        #     {BodyFieldnames.LabVisit: "u2"}, f"ID IN ({uuid1}, {uuid2})"
        # )
        # u2_sql = (
        #     f"SELECT * FROM mainTable WHERE {BodyFieldnames.LabVisit} = 'u2' ORDER BY ID ASC"
        # )
        # records = await database.query(u2_sql)
        # assert len(records) == 2, "%s count" % u2_sql
