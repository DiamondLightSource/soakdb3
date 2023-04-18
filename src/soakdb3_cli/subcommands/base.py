import logging
import os
import tempfile
from typing import Optional

# Configurator.
from dls_multiconf_lib.constants import ThingTypes as MulticonfThingTypes
from dls_multiconf_lib.multiconfs import Multiconfs, multiconfs_set_default

# Utilities.
from dls_utilpack.visit import get_visit_year

# Environment variables with some extra functionality.
from soakdb3_lib.envvar import Envvar

logger = logging.getLogger(__name__)


class ArgKeywords:
    CONFIGURATION = "configuration"


class Base:
    """
    Base class for femtocheck subcommands.  Handles details like configuration.
    """

    def __init__(self, args):
        self._args = args

        self.__temporary_directory = None

    # ----------------------------------------------------------------------------------------
    def get_multiconf(self, args_dict: dict):

        soakdb3_multiconf = self.build_object_from_environment(args_dict=args_dict)

        # For convenience, make a temporary directory for this test.
        self.__temporary_directory = tempfile.TemporaryDirectory()

        # Make the temporary directory available to the multiconf.
        soakdb3_multiconf.substitute(
            {"temporary_directory": self.__temporary_directory.name}
        )

        substitutions = {
            "CWD": os.getcwd(),
            "HOME": os.environ.get("HOME", "HOME"),
            "USER": os.environ.get("USER", "USER"),
            "PATH": os.environ.get("PATH", "PATH"),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "PYTHONPATH"),
        }

        if hasattr(self._args, "visit") and self._args.visit != "VISIT":
            BEAMLINE = os.environ.get("BEAMLINE")
            if BEAMLINE is None:
                raise RuntimeError("BEAMLINE environment variable is not defined")
            year = get_visit_year(BEAMLINE, self._args.visit)
            substitutions["BEAMLINE"] = BEAMLINE
            substitutions["VISIT"] = self._args.visit
            substitutions["YEAR"] = year

        soakdb3_multiconf.substitute(substitutions)

        # Set this as the default multiconf so it is available everywhere.
        multiconfs_set_default(soakdb3_multiconf)

        return soakdb3_multiconf

    # ----------------------------------------------------------------------------------------
    def build_object_from_environment(
        self,
        environ: Optional[dict] = None,
        args_dict: Optional[dict] = None,
    ):

        configuration_keyword = "configuration"

        multiconf_filename = None

        if args_dict is not None:
            multiconf_filename = args_dict.get(configuration_keyword)

        if multiconf_filename is not None:
            # Make sure the path exists.
            if not os.path.exists(multiconf_filename):
                raise RuntimeError(
                    f"unable to find --{configuration_keyword} file {multiconf_filename}"
                )
        else:
            # Get the explicit name of the config file.
            multiconf_filename = Envvar(
                Envvar.SOAKDB3_CONFIGFILE,
                environ=environ,
            )

            # Config file is explicitly named?
            if multiconf_filename.is_set:
                # Make sure the path exists.
                multiconf_filename = multiconf_filename.value
                if not os.path.exists(multiconf_filename):
                    raise RuntimeError(
                        f"unable to find {Envvar.SOAKDB3_CONFIGFILE} {multiconf_filename}"
                    )
            # Config file is not explicitly named?
            else:
                raise RuntimeError(
                    f"command line --{configuration_keyword} not given"
                    f" and environment variable {Envvar.SOAKDB3_CONFIGFILE} is not set"
                )

        multiconf = Multiconfs().build_object(
            {
                "type": MulticonfThingTypes.YAML,
                "type_specific_tbd": {"filename": multiconf_filename},
            }
        )

        return multiconf
