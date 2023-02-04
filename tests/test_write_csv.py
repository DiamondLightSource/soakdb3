import csv
import logging

# Object managing datafaces.
from soakdb3_api.datafaces.datafaces import datafaces_get_default

# Context creator.
from soakdb3_lib.contexts.contexts import Contexts

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestWriteCsv:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/laptop.yaml"
        WriteCsvTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class WriteCsvTester(BaseContextTester):
    """
    Class to test the write_csv API call through the server.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """

        configurator = self.get_configurator()

        context_configuration = await configurator.load()
        context = Contexts().build_object(context_configuration)

        # The visitid to match what is in the test configuration yaml.
        visitid = output_directory

        async with context:
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
