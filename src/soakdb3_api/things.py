import json

# Use standard logging in this module.
import logging

# Method to import a class from a file.
from dls_utilpack.import_class import import_class

# Exceptions.
from soakdb3_api.exceptions import DuplicateUuidException, NotFound

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
class Things:
    """
    Class managing list of things.
    """

    def __init__(self, name):
        self._name = name
        self._list = []
        self._dict = {}

    # -----------------------------------------------------------------------------
    def name(self):
        return self._name

    # -----------------------------------------------------------------------------
    def list(self):
        return self._list

    # -----------------------------------------------------------------------------
    def clear(self):
        self._list = []
        self._dict = {}

    # -----------------------------------------------------------------------------
    def len(self):
        return len(self._list)

    # -----------------------------------------------------------------------------
    def add(self, things):
        if not hasattr(things, "__iter__"):
            things = [things]

        for thing in things:
            if thing.uuid() not in self._dict:
                self._list.append(thing)
                self._dict[thing.uuid()] = thing
            else:
                raise DuplicateUuidException(
                    "%s not adding duplicate %s uuid %s"
                    % (self._name, thing.thing_type(), thing.uuid())
                )

    # -----------------------------------------------------------------------------
    def find(self, key, trait_name=None):
        if trait_name is None:
            if key in self._dict:
                return self._dict[key]
            raise NotFound("%s list does not have uuid %s" % (self._name, key))
        else:
            for thing in self._list:
                if thing.trait(trait_name) == key:
                    return thing
            raise NotFound(
                "%s list does not have %s %s" % (self._name, trait_name, key)
            )

    # -----------------------------------------------------------------------------
    def has(self, uuid):
        return uuid in self._dict

    # -----------------------------------------------------------------------------
    # If a string, parse for json, yaml or whatever.
    def parse_specification(self, specification):
        if isinstance(specification, dict):
            return specification

        if isinstance(specification, str):
            return json.loads(specification)

        raise RuntimeError(
            "specification is a %s but needs to be a dict or a string"
            % (type(specification).__name__)
        )

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        # This looks like a request to load a class at runtime?
        # The class type should be filename::classname.
        if "::" in class_type:

            RuntimeClass = import_class(class_type)

            return RuntimeClass

        raise NotFound("unable to get class for %s thing" % (class_type))
