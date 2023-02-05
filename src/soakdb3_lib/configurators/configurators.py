# Use standard logging in this module.
import logging
import os
from typing import Optional

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.require import require

# Exceptions.
from soakdb3_api.exceptions import NotFound

# Class managing list of things.
from soakdb3_api.things import Things

# Environment variables with some extra functionality.
from soakdb3_lib.envvar import Envvar

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------------
__default_configurator = None


def configurators_set_default(configurator):
    global __default_configurator
    __default_configurator = configurator


def configurators_get_default():
    global __default_configurator
    if __default_configurator is None:
        raise RuntimeError("configurators_get_default instance is None")
    return __default_configurator


def configurators_has_default():
    global __default_configurator
    return __default_configurator is not None


# -----------------------------------------------------------------------------------------


class Configurators(Things):
    """
    Configuration loader.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        configurator_class = self.lookup_class(
            require(f"{callsign(self)} specification", specification, "type")
        )

        try:
            configurator_object = configurator_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to instantiate configurator object from module %s"
                % (configurator_class.__module__)
            ) from exception

        return configurator_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        if class_type == "soakdb3_lib.configurators.yaml":
            from soakdb3_lib.configurators.yaml import Yaml

            return Yaml

        raise NotFound("unable to get configurator class for type %s" % (class_type))

    # ----------------------------------------------------------------------------------------
    def build_object_from_environment(
        self,
        environ: Optional[dict] = None,
        args_dict: Optional[dict] = None,
    ):

        configuration_keyword = "configuration"

        configurator_filename = None

        if args_dict is not None:
            configurator_filename = args_dict.get(configuration_keyword)

        if configurator_filename is not None:
            # Make sure the path exists.
            if not os.path.exists(configurator_filename):
                raise RuntimeError(
                    f"unable to find --{configuration_keyword} file {configurator_filename}"
                )
        else:
            # Get the explicit name of the config file.
            bxflow_configfile = Envvar(
                Envvar.SOAKDB3_CONFIGFILE,
                environ=environ,
            )

            # Config file is explicitly named?
            if bxflow_configfile.is_set:
                # Make sure the path exists.
                configurator_filename = bxflow_configfile.value
                if not os.path.exists(configurator_filename):
                    raise RuntimeError(
                        f"unable to find {Envvar.SOAKDB3_CONFIGFILE} {configurator_filename}"
                    )
            # Config file is not explicitly named?
            else:
                raise RuntimeError(
                    f"command line --{configuration_keyword} not given"
                    f" and environment variable {Envvar.SOAKDB3_CONFIGFILE} is not set"
                )
        configurator = self.build_object(
            {
                "type": "soakdb3_lib.configurators.yaml",
                "type_specific_tbd": {"filename": configurator_filename},
            }
        )

        configurator.substitute(
            {"configurator_directory": os.path.dirname(configurator_filename)}
        )

        return configurator
