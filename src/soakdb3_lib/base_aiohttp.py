import logging

from dls_servbase_lib.base_aiohttp import BaseAiohttp as DlsServbaseBaseAiohttp

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------
class BaseAiohttp(DlsServbaseBaseAiohttp):
    """
    Object representing a a process which receives requests from aiohttp.
    """

    pass
