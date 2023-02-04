import logging

# Class for an aiohttp client.
from soakdb3_api.aiohttp_client import AiohttpClient

# XchemBeDataface protocolj things.
from soakdb3_api.datafaces.constants import Commands, Keywords

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------
class Aiohttp:
    """
    Object implementing client side API for talking to the dataface server.
    Please see doctopic [A01].
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):
        self.__specification = specification

        self.__aiohttp_client = AiohttpClient(
            specification["type_specific_tbd"]["aiohttp_specification"],
        )

    # ----------------------------------------------------------------------------------------
    def specification(self):
        return self.__specification

    # ----------------------------------------------------------------------------------------
    async def backup(self, visitid):
        """"""
        return await self.__send_protocolj("backup", visitid)

    # ----------------------------------------------------------------------------------------
    async def restore(self, visitid, nth):
        """"""
        return await self.__send_protocolj("restore", visitid, nth)

    # ----------------------------------------------------------------------------------------
    async def query(self, visitid, sql, subs=None, why=None):
        """"""
        return await self.__send_protocolj("query", visitid, sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def query_for_dictionary(self, visitid, sql, subs=None, why=None):
        """"""
        return await self.__send_protocolj(
            "query_for_dictionary", visitid, sql, subs=subs, why=why
        )

    # ----------------------------------------------------------------------------------------
    async def execute(self, visitid, sql, subs=None, why=None):
        """"""
        return await self.__send_protocolj("execute", visitid, sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def insert(self, visitid, table_name, records, subs=None, why=None):
        """"""
        return await self.__send_protocolj(
            "insert", visitid, table_name, records, subs=subs, why=why
        )

    # ----------------------------------------------------------------------------------------
    async def update(self, visitid, table_name, record, where, subs=None, why=None):
        """"""
        return await self.__send_protocolj(
            "update", visitid, table_name, record, where, subs=subs, why=why
        )

    # ----------------------------------------------------------------------------------------
    async def update_head_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """

        return await self.__send_protocolj("update_head_fields", visitid, fields)

    # ----------------------------------------------------------------------------------------
    async def update_body_fields(self, visitid, fields):
        """
        Handle update request from a soakdb range change.
        """

        return await self.__send_protocolj("update_body_fields", visitid, fields)

    # ----------------------------------------------------------------------------------------
    async def write_csv(self, visitid, rows, filename):
        """
        Handle request to write rows as csv file.

        The rows are assumed fully prepared ahead of time.

        The filename's path should be a subdirectory (no leading slash).

        """

        return await self.__send_protocolj("write_csv", visitid, rows, filename)

    # ----------------------------------------------------------------------------------------
    async def report_health(self):
        """"""
        return await self.__send_protocolj("report_health")

    # ----------------------------------------------------------------------------------------
    async def __send_protocolj(self, function, *args, **kwargs):
        """"""

        return await self.__aiohttp_client.client_protocolj(
            {
                Keywords.COMMAND: Commands.EXECUTE,
                Keywords.PAYLOAD: {
                    "function": function,
                    "args": args,
                    "kwargs": kwargs,
                },
            },
        )

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""

        if self.__aiohttp_client is not None:
            await self.__aiohttp_client.close_client_session()

    # ----------------------------------------------------------------------------------------
    async def client_report_health(self):
        """"""

        return await self.__aiohttp_client.client_report_health()
