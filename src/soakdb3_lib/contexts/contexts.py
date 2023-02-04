# Use standard logging in this module.
import logging

import yaml

# Exceptions.
from soakdb3_api.exceptions import NotFound

# Class managing list of things.
from soakdb3_api.things import Things

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------------


class Contexts(Things):
    """
    Context loader.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        if not isinstance(specification, dict):
            with open(specification, "r") as yaml_stream:
                specification = yaml.safe_load(yaml_stream)

        xchem_be_context_class = self.lookup_class(specification["type"])

        try:
            xchem_be_context_object = xchem_be_context_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build xchem_be_context object for type %s"
                % (xchem_be_context_class)
            ) from exception

        return xchem_be_context_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        if class_type == "soakdb3_lib.contexts.classic":
            from soakdb3_lib.contexts.classic import Classic

            return Classic

        raise NotFound(
            "unable to get xchem_be_context class for type %s" % (class_type)
        )
