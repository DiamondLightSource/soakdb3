# Use standard logging in this module.
import logging
import uuid
from typing import Any, Dict

# Exeptions.
from soakdb3_api.exceptions import NotFound

logger = logging.getLogger()


# -----------------------------------------------------------------------------
class Thing:
    """
    Class for a named thing with traits.
    """

    def __init__(self, thing_type: str, specification, predefined_uuid=None):
        self.__thing_type = thing_type
        self.__specification = specification
        self.__uuid = predefined_uuid
        if self.__uuid is None:
            self.__uuid = str(uuid.uuid4())
        self.__state = None
        self.__traits: Dict[str, Any] = {}

    # -----------------------------------------------------------------------------
    def __str__(self):
        return self.__thing_type

    # -----------------------------------------------------------------------------
    def specification(self, specification=None):
        if specification is not None:
            self.__specification = specification

        return self.__specification

    # -----------------------------------------------------------------------------
    def thing_type(self):
        return self.__thing_type

    # -----------------------------------------------------------------------------
    def set_thing_type(self, thing_type):
        self.__thing_type = thing_type

    # -----------------------------------------------------------------------------
    def uuid(self):
        return self.__uuid

    # -----------------------------------------------------------------------------
    def state(self, state=None):
        """
        Deprecated.
        """
        if state is not None:
            self.__state = state
        return self.__state

    # -----------------------------------------------------------------------------
    def set_state(self, state):
        self.__state = state

    # -----------------------------------------------------------------------------
    def get_state(self):
        return self.__state

    # -----------------------------------------------------------------------------
    def traits(self):
        return self.__traits

    # -----------------------------------------------------------------------------
    def trait(self, trait_name):
        """
        Return value of trait if exists, otherwise raise NotFound.
        """

        if trait_name not in self.__traits:
            raise NotFound("%s has no trait %s" % (self.__name, trait_name))

        return self.__traits[trait_name]
