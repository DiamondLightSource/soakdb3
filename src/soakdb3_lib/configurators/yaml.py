import logging
import re
from string import Template

import yaml

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.explain import explain2
from dls_utilpack.require import require
from dls_utilpack.substitute import substitute_string

# Exceptions.
from soakdb3_api.exceptions import NotFound

# Base class which maps flask requests to methods.
from soakdb3_lib.configurators.base import Base

logger = logging.getLogger(__name__)


thing_type = "soakdb3_lib.configurators.yaml"


class DottedTemplate(Template):
    """
    Allow tokens to have "." in them.
    """

    idpattern = r"(?a:[_.a-z][_.a-z0-9]*)"


class Yaml(Base):
    """
    Object representing a configurator which loads a yaml file.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):
        self.__filename = "unknown filename"

        Base.__init__(self, thing_type, specification)

        type_specific_tbd = require(
            f"{callsign(self)} specification", specification, "type_specific_tbd"
        )

        self.__filename = require(
            f"{callsign(self)} specification type_specific_tbd",
            type_specific_tbd,
            "filename",
        )

        self.__removals = []
        self.__substitutions = {}
        self.__last_loaded_dict = {}

    # ----------------------------------------------------------------------------------------
    def callsign(self):
        return f"XchemBeConfigurator.Yaml {self.__filename}"

    # ----------------------------------------------------------------------------------------
    def require(self, keyword):
        parts = keyword.split(".")

        pointer = self.__last_loaded_dict

        for index, part in enumerate(parts):
            if not isinstance(pointer, dict):
                if index == len(parts) - 1:
                    raise NotFound(f"{callsign(self)} found non-dict at {keyword}")
                else:
                    raise NotFound(
                        f"{callsign(self)} found non-dict at %s when looking for %s"
                        % (".".join(parts[: index + 1]), keyword)
                    )

            if part in pointer:
                pointer = pointer[part]
            else:
                if index == len(parts) - 1:
                    raise NotFound(
                        f"{callsign(self)} is unable to find keyword {keyword}"
                    )
                else:
                    raise NotFound(
                        f"{callsign(self)} is unable to find keyword %s when looking for %s"
                        % (".".join(parts[: index + 1]), keyword)
                    )

        return pointer

    # ----------------------------------------------------------------------------------------
    def substitute(self, substitutions):
        self.__substitutions.update(substitutions)

    # ----------------------------------------------------------------------------------------
    def remove(self, removals):
        if isinstance(removals, list):
            self.__removals.extend(removals)
        else:
            self.__removals.append(removals)

    # ----------------------------------------------------------------------------------------
    async def load(self):
        try:
            with open(self.__filename, "r") as yaml_stream:
                loaded_string = yaml_stream.read()
        except Exception as exception:
            raise RuntimeError(f"unable to read {self.__filename}") from exception

        # Apply the substitutions to symbols in the loaded string.
        loaded_string = substitute_string(
            loaded_string, self.__substitutions, what=callsign(self)
        )

        try:
            loaded_dict = yaml.safe_load(loaded_string)
        except Exception as exception:
            raise RuntimeError(f"unable to parse {self.__filename}") from exception

        # Apply requested removals to the dict after parsing.
        self.__apply_removals(loaded_dict, self.__removals)

        self.__last_loaded_dict = loaded_dict

        return loaded_dict

    # ----------------------------------------------------------------------------------------
    def __apply_removals(self, loaded_dict, removals):
        for removal in removals:
            if removal in loaded_dict:
                loaded_dict.pop(removal)

    # ----------------------------------------------------------------------------------------
    def resolve(self, target):
        """
        Use the internal substitutions to resolve tokens in the given string.
        For example "${multi.level1.level2}".  See test_configurator for example.
        """

        if target is None:
            return None

        # Only a string can really have the dotted notation in it.
        # TODO: Extend configurator resolve to allow substitution in dicts.
        if not isinstance(target, str):
            return target

        try:
            # The regex which finds the ${tokens}.
            regex = re.compile(r"\$\{([^\}]+)")

            # Find all the tokens, eliciting the variable names.
            tokens = regex.findall(target)

            # Make the substitutions from within our current configuration state.
            substitutions = {}
            for index, token in enumerate(tokens):
                substitutions[token] = self.require(token)

            # Apply subtitutions to the target.
            return substitute_string(target, substitutions, what=callsign(self))
        except Exception as exception:
            raise RuntimeError(
                explain2(exception, f"{callsign(self)} substituting {target}")
            )
