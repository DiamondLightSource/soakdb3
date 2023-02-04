import logging

from dls_utilpack.callsign import callsign

# Utilities.
from dls_utilpack.explain import explain

# Base class which maps flask requests to methods.
from soakdb3_lib.contexts.base import Base

# Contexts.
from soakdb3_lib.datafaces.context import Context as XchemBeDatafaceContext

logger = logging.getLogger(__name__)


thing_type = "soakdb3_lib.contexts.classic"


class Classic(Base):
    """
    Object representing an event dataface connection.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):
        Base.__init__(self, thing_type, specification)

        self.__dataface = None

    # ----------------------------------------------------------------------------------------
    async def __aenter__(self):
        """ """
        logger.debug(f"entering {callsign(self)} context")

        try:

            try:
                specification = self.specification().get("dataface_specification")
                if specification is not None:
                    logger.debug(f"at entering position {callsign(self)} DATAFACE")
                    self.__dataface = XchemBeDatafaceContext(specification)
                    await self.__dataface.aenter()
            except Exception as exception:
                raise RuntimeError(
                    explain(exception, f"creating {callsign(self)} dataface context")
                )

        except Exception as exception:
            await self.aexit()
            raise RuntimeError(explain(exception, f"entering {callsign(self)} context"))

        logger.debug(f"entered {callsign(self)} context")

    # ----------------------------------------------------------------------------------------
    async def __aexit__(self, type, value, traceback):
        """ """

        await self.aexit()

    # ----------------------------------------------------------------------------------------
    async def aexit(self):
        """ """

        logger.debug(f"exiting {callsign(self)} context")

        if self.__dataface is not None:
            logger.debug(f"at exiting position {callsign(self)} DATAFACE")
            try:
                await self.__dataface.aexit()
            except Exception as exception:
                logger.error(
                    explain(exception, f"exiting {callsign(self.__dataface)} context"),
                    exc_info=exception,
                )
            self.__dataface = None

        logger.debug(f"exited {callsign(self)} context")

    # ----------------------------------------------------------------------------------------
    async def __dead_or_alive(self, context, dead, alive):

        if context is not None:
            try:
                # A server was defined for this context?
                if await context.is_process_started():
                    if await context.is_process_alive():
                        alive.append(context)
                    else:
                        dead.append(context)
            except Exception:
                raise RuntimeError(
                    f"unable to determine dead or alive for context {callsign(context)}"
                )

    # ----------------------------------------------------------------------------------------
    async def __dead_or_alive_all(self):
        """
        Return two lists, one for dead and one for alive processes.
        TODO: Parallelize context process alive/dead checking.
        """

        dead = []
        alive = []

        await self.__dead_or_alive(self.__dataface, dead, alive)

        return dead, alive

    # ----------------------------------------------------------------------------------------
    async def is_any_process_alive(self):
        """
        Check all configured processes, return if any alive.
        """
        dead, alive = await self.__dead_or_alive_all()

        # logger.debug(f"[PIDAL] {len(dead)} processes are dead, {len(alive)} are alive")

        return len(alive) > 0

    # ----------------------------------------------------------------------------------------
    async def is_any_process_dead(self):
        """
        Check all configured processes, return if any alive.
        """
        dead, alive = await self.__dead_or_alive_all()

        return len(dead) > 0
