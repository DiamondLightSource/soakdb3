import logging

# Base class for all aiosqlite database objects.
from soakdb3_lib.databases.table_definitions import BodyTable, HeadTable, VisitTable

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class DatabaseDefinition:
    """
    Class which defines the database tables and revision migration path.
    Used in concert with the normsql class.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self):
        """
        Construct object.  Do not connect to database.
        """

        self.LATEST_REVISION = 1

    # ----------------------------------------------------------------------------------------
    async def add_table_definitions(self):
        """
        Make all the table definitions.
        """

        # Table schemas in our database.
        self.add_table_definition(HeadTable())
        self.add_table_definition(BodyTable())
        self.add_table_definition(VisitTable())
