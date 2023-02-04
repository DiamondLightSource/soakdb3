import logging
import os

# Configurator.
from soakdb3_lib.configurators.configurators import (
    Configurators,
    configurators_set_default,
)


class ArgKeywords:
    CONFIGURATION = "configuration"


logger = logging.getLogger(__name__)


class Base:
    """
    Base class for femtocheck subcommands.  Handles details like configuration.
    """

    def __init__(self, args):
        self._args = args

        self.__temporary_directory = None

    # ----------------------------------------------------------------------------------------
    def get_configurator(self, args_dict: dict):

        configurator = Configurators().build_object_from_environment(
            args_dict=args_dict
        )

        substitutions = {
            "CWD": os.getcwd(),
            "HOME": os.environ.get("HOME", "HOME"),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "PYTHONPATH"),
            "USER": os.environ.get("USER", "USER"),
        }

        configurator.substitute(substitutions)

        # Set this as the default configurator so it is available everywhere.
        configurators_set_default(configurator)

        return configurator
