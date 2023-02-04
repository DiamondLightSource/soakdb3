import logging

# Base class for a Thing which has a name and traits.
from soakdb3_api.thing import Thing

logger = logging.getLogger(__name__)


class Base(Thing):
    """ """

    # ----------------------------------------------------------------------------------------
    def __init__(self, thing_type, specification=None, predefined_uuid=None):
        Thing.__init__(self, thing_type, specification, predefined_uuid=predefined_uuid)

        self.__logging_mpqueue = None

    # ----------------------------------------------------------------------------------------
    def set_logging_mpqueue(self, mpqueue):
        self.__logging_mpqueue = mpqueue

    def get_logging_mpqueue(self):
        return self.__logging_mpqueue
