# Use standard logging in this module.
import logging

# Class managing list of things.
from dls_utilpack.things import Things

# Exceptions.
from soakdb3_api.exceptions import NotFound

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------


class Datafaces(Things):
    """
    List of available datafaces.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        dataface_class = self.lookup_class(specification["type"])

        try:
            dataface_object = dataface_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build dataface object for type %s" % (dataface_class)
            ) from exception

        return dataface_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        if class_type == "soakdb3_lib.datafaces.aiohttp":
            from soakdb3_lib.datafaces.aiohttp import Aiohttp

            return Aiohttp

        elif class_type == "soakdb3_lib.datafaces.aiosqlite":
            from soakdb3_lib.datafaces.aiosqlite import Aiosqlite

            return Aiosqlite

        raise NotFound("unable to get dataface class for type %s" % (class_type))
