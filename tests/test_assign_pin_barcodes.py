import csv
import logging

from soakdb3_api.databases.constants import BodyFieldnames, PinBarcodeErrors, Tablenames

# Client context creator.
from soakdb3_api.datafaces.context import Context as Soakdb3DatafaceClientContext
from soakdb3_api.datafaces.datafaces import datafaces_get_default

# Server context creator.
from soakdb3_lib.datafaces.context import Context as Soakdb3DatafaceServerContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestAssignPinBarcodes:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/services.yaml"
        AssignPinBarcodesTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class AssignPinBarcodesTester(BaseContextTester):
    """
    Class to test the write_csv API call through the server.
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
                await self.__run_the_csv_test(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_the_csv_test(self, constants, output_directory):
        """ """

        # The visitid to match what is in the test configuration yaml.
        visitid = output_directory

        dataface = datafaces_get_default()

        uuid1 = 1000

        dataface = datafaces_get_default()

        # First record is good.
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.ID: uuid1,
                    BodyFieldnames.Puck: "IN-0093",
                    BodyFieldnames.PuckPosition: 3,
                }
            ],
        )

        # Next record is a bad puck.
        uuid1 += 1
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.ID: uuid1,
                    BodyFieldnames.Puck: "ZZ-0093",
                    BodyFieldnames.PuckPosition: 3,
                }
            ],
        )

        # Next record is a bad pin integer.
        uuid1 += 1
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.ID: uuid1,
                    BodyFieldnames.Puck: "IN-0093",
                    BodyFieldnames.PuckPosition: "X",
                }
            ],
        )

        # Next record is a bad pin number..
        uuid1 += 1
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.ID: uuid1,
                    BodyFieldnames.Puck: "IN-0093",
                    BodyFieldnames.PuckPosition: 16,
                }
            ],
        )

        # Next record is a can't find (from the csv file itself).
        uuid1 += 1
        await dataface.insert(
            visitid,
            Tablenames.BODY,
            [
                {
                    BodyFieldnames.ID: uuid1,
                    BodyFieldnames.Puck: "IN-0093",
                    BodyFieldnames.PuckPosition: 10,
                }
            ],
        )

        # Assign the barcodes.
        await dataface.assign_pin_barcodes(visitid)

        # Check the results.
        all_sql = f"SELECT * FROM {Tablenames.BODY} ORDER BY ID ASC"

        records = await dataface.query_for_dictionary(visitid, all_sql)
        assert len(records) == 5

        record = records[0]
        assert record["PinBarcode"] == "IN150E0735"

        record = records[1]
        assert record["PinBarcode"] == PinBarcodeErrors.NO_PUCK

        record = records[2]
        assert record["PinBarcode"] == PinBarcodeErrors.BAD_INT

        record = records[3]
        assert record["PinBarcode"] == PinBarcodeErrors.BAD_PIN

        record = records[4]
        assert record["PinBarcode"] == PinBarcodeErrors.CANT_FIND
