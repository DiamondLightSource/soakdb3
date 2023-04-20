from typing import Optional

from pydantic import BaseModel


class CrystalWellModel(BaseModel):
    """
    Model representing enough fields to inject desired crystal wells into the soadkb3 Main table.

    Typically this structure is used to inject new wells and their echo locations to soakdb3.

    ID is ignored when appending crystal wells, but populated by a fetch.
    """

    ID: Optional[str] = None
    LabVisit: str
    CrystalPlate: str
    CrystalWell: str
    EchoX: int
    EchoY: int
