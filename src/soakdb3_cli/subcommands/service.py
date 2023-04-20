import asyncio

# Use standard logging in this module.
import logging

# Base class for cli subcommands.
from soakdb3_cli.subcommands.base import ArgKeywords, Base

# Context creator.
from soakdb3_lib.datafaces.context import Context

logger = logging.getLogger()


# --------------------------------------------------------------
class Service(Base):
    """
    Start single service and keep running until ^C or remotely requested shutdown.
    """

    def __init__(self, args, mainiac):
        super().__init__(args)

    # ----------------------------------------------------------------------------------------
    def run(self):
        """ """

        # Run in asyncio event loop.
        asyncio.run(self.__run_coro())

    # ----------------------------------------------------------
    async def __run_coro(self):
        """"""

        # Load the configuration.
        multiconf = self.get_multiconf(vars(self._args))
        configuration = await multiconf.load()

        # Make a client context for the soakdb3 service.
        soakdb3_context = Context(configuration["soakdb3_dataface_specification"])

        # Open the context which starts the service process.
        async with soakdb3_context:
            # Wait for it to finish.
            await soakdb3_context.server.wait_for_shutdown()

    # ----------------------------------------------------------
    def add_arguments(parser):

        parser.add_argument(
            "--configuration",
            "-c",
            help="Configuration file.",
            type=str,
            metavar="yaml filename",
            default=None,
            dest=ArgKeywords.CONFIGURATION,
        )

        return parser
