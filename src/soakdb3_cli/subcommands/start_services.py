import asyncio

# Use standard logging in this module.
import logging

# Utilities.
from dls_utilpack.describe import describe

# Base class for cli subcommands.
from soakdb3_cli.subcommands.base import ArgKeywords, Base

# Context creator.
from soakdb3_lib.contexts.contexts import Contexts

logger = logging.getLogger()

# Specifications of services we can start, and their short names for parse args.
services = {
    "dataface_specification": "dataface",
}


# --------------------------------------------------------------
class StartServices(Base):
    """
    Start one or more services and keep them running until ^C.
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
        configurator = self.get_configurator(vars(self._args))

        # Let the configurator know about any mpqueue logging.
        # configurator.set_logging_mpqueue(self.__mainiac.mpqueue)

        context_configuration = await configurator.load()

        if len(self._args.service_names) == 0:
            self._args.service_names = ["all"]

        if "all" in self._args.service_names:
            selected_service_names = []
            for _, service_name in services.items():
                selected_service_names.append(service_name)
        else:
            selected_service_names = self._args.service_names

        logger.debug(describe("selected_service_names", selected_service_names))

        # Change all start_as to None, except the one we are starting.
        for keyword, specification in context_configuration.items():
            if keyword in services:
                service_name = services[keyword]
                if service_name in selected_service_names:
                    specification["context"] = {"start_as": "process"}

        # Make a context from the configuration.
        context = Contexts().build_object(context_configuration)

        # Open the context (servers and clients).
        async with context:
            try:
                # Stay up until all processes are dead.
                # TODO: Use asyncio wait or sentinel for all started processes to be dead.
                while True:
                    await asyncio.sleep(1.0)
                    if not await context.is_any_process_alive():
                        logger.info("all processes have shutdown")
                        break
            except KeyboardInterrupt:
                pass

    # ----------------------------------------------------------
    def add_arguments(parser):

        services_list = list(services.values())

        parser.add_argument(
            help='"all" (default) or any combination of {%s}'
            % (" ".join(services_list)),
            nargs="*",
            type=str,
            metavar="service name(s)",
            dest="service_names",
            default=[],
        )

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
