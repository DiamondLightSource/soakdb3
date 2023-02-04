import asyncio
import logging
import multiprocessing

import pytest

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class BaseSpecificationTester:
    """
    This is a base class for tests which take a specification.
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
