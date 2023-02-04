import logging
import os
import shutil

import pytest

# Formatting of testing log messages.
from dls_logformatter.dls_logformatter import DlsLogformatter

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def constants(request):

    constants = {}

    yield constants


# --------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def logging_setup():

    formatter = DlsLogformatter(type="long")
    logger = logging.StreamHandler()
    logger.setFormatter(formatter)
    logging.getLogger().addHandler(logger)

    # Log level for all modules.
    logging.getLogger().setLevel("DEBUG")

    # Turn off noisy debug.
    logging.getLogger("asyncio").setLevel("WARNING")
    logging.getLogger("pika").setLevel("WARNING")
    logging.getLogger("stomp").setLevel("WARNING")
    logging.getLogger("luigi-interface").setLevel("WARNING")
    logging.getLogger("luigi.xchem_be_scheduler").setLevel("INFO")
    logging.getLogger("urllib3.connectionpool").setLevel("INFO")

    logging.getLogger("soakdb3_lib.things").setLevel("INFO")

    # Messages about starting and stopping services.
    logging.getLogger("soakdb3_lib.base_aiohttp").setLevel("INFO")

    # All xchem_be database sql commands.
    # logging.getLogger("soakdb3_lib.databases.aiosqlite").setLevel("INFO")

    logging.getLogger("soakdb3_lib.contexts.classic").setLevel("INFO")
    logging.getLogger("soakdb3_lib.datafaces.context").setLevel("INFO")

    # Registering signal handler.
    logging.getLogger("dls_siggy_lib.signal").setLevel("INFO")

    # Set filter on the ispyb logger to ignore the annoying NOTICE.
    logging.getLogger("ispyb").addFilter(_ispyb_logging_filter())

    # Cover the version.
    # logger.info("\n%s", (json.dumps(version_meta(), indent=4)))

    yield None


# --------------------------------------------------------------------------------
class _traitlets_logging_filter:
    """
    Python logging filter to remove annoying traitlets messages.
    These are not super useful to see all the time at the DEBUG level.
    """

    def filter(self, record):

        if record.levelno == 10:
            if "jupyter_client/client.py" in record.pathname:
                return 0
            if "jupyter_client/connect.py" in record.pathname:
                return 0
            if "jupyter_client/manager.py" in record.pathname:
                return 0
            if "jupyter_client/provisioning/factory.py" in record.pathname:
                return 0
            if "nbclient/client.py" in record.pathname:
                return 0
            if "nbconvert/exporters/templateexporter.py" in record.pathname:
                return 0
            if "nbconvert/preprocessors/base.py" in record.pathname:
                return 0
            if "/nbconvert/preprocessors/coalescestreams.py" in record.pathname:
                return 0

            # if "" in record.pathname:
            #     return 0

        return 1


# --------------------------------------------------------------------------------
class _ispyb_logging_filter:
    """
    Python logging filter to remove annoying traitlets messages.
    These are not super useful to see all the time at the DEBUG level.
    """

    def filter(self, record):

        if record.msg.startswith(
            "NOTICE: This code uses __future__ functionality in the ISPyB API."
        ):
            return 0

        return 1


# --------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def output_directory(request):
    # TODO: Better way to get a newline in conftest after pytest emits the test class name.
    print("")

    # Tmp directory which we can write into.
    output_directory = "/tmp/%s/%s/%s" % (
        "/".join(__file__.split("/")[-3:-1]),
        request.cls.__name__,
        request.function.__name__,
    )

    # Tmp directory which we can write into.
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory, ignore_errors=False, onerror=None)
    os.makedirs(output_directory)

    # logger.debug("output_directory is %s" % (output_directory))

    yield output_directory
