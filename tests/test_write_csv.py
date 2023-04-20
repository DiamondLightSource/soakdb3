import csv
import logging

# Client context creator.
from soakdb3_api.datafaces.context import Context as Soakdb3DatafaceClientContext
from soakdb3_api.datafaces.datafaces import datafaces_get_default

# Server context creator.
from soakdb3_lib.datafaces.context import Context as Soakdb3DatafaceServerContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestWriteCsv:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/services.yaml"
        WriteCsvTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class WriteCsvTester(BaseContextTester):
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

        data = [
            ["a", "1"],
            ["b", "2"],
            ["c", '"3"'],
            ["d", "4,5,6"],
            ["e", "line1\nline2"],
            ["f", ""],
            ["g"],
            ["h", "done"],
        ]

        filename = "echo/Batchfile.csv"

        # Write csv.
        await dataface.write_csv(visitid, data, filename)

        # Read csv.
        fieldnames = [0, 1]
        restval = "none"
        with open(f"{output_directory}/lab36/{filename}") as stream:
            reader = csv.DictReader(stream, fieldnames=fieldnames, restval=restval)
            i = 0
            for row in reader:
                for col, value in row.items():
                    # Data row has at least this many columns?
                    if col < len(data[i]):
                        assert value == data[i][col], f"line {i} column {col}"
                    else:
                        assert value == restval, f"line {i} column {col}"
                i = i + 1
