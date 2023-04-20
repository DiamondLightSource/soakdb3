# Use standard logging in this module.
import logging

# Base class.
from dls_utilpack.thing import Thing

logger = logging.getLogger()


# -----------------------------------------------------------------------------
class Context(Thing):
    """
    Class for an asyncio context.
    For now, it's just a Thing with two extra public methods for enter and exit.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, thing_type, specification):
        Thing.__init__(self, thing_type, specification)

    # ----------------------------------------------------------------------------------------
    async def __aenter__(self):
        """ """

        await self.aenter()

    # ----------------------------------------------------------------------------------------
    async def __aexit__(self, type, value, traceback):
        """ """

        await self.aexit()
