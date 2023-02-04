import asyncio
import logging
import multiprocessing

import pytest

logger = logging.getLogger(__name__)


class Base:

    # ----------------------------------------------------------------------------------------
    def main(self, constants, infrastrcuture_context, output_directory):
        """ """

        multiprocessing.current_process().name = "main"

        failure_message = None
        try:
            # Run main test in asyncio event loop.
            asyncio.run(
                self._main_coroutine(
                    constants, infrastrcuture_context, output_directory
                )
            )

        except Exception as exception:
            logger.exception(
                "unexpected exception in the test method", exc_info=exception
            )
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)
