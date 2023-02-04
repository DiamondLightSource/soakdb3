"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from typing import Optional

import dls_mainiac_lib.version
import dls_servbase_lib.version
import dls_utilpack.version

from soakdb3_lib import __version__


# ----------------------------------------------------------
def version() -> str:
    """
    Version of the soakdb3 package as a string.
    """

    return __version__


# ----------------------------------------------------------
def meta(given_meta: Optional[dict] = None) -> dict:
    """
    Returns version information from the soakdb3 package
    and its dependencies as a dict.
    Adds version information to a given meta dict if it was provided.
    """

    meta = {}
    meta["soakdb3_lib"] = version()
    meta.update(dls_servbase_lib.version.meta())
    meta.update(dls_mainiac_lib.version.meta())
    meta.update(dls_utilpack.version.meta())

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta
    return given_meta
