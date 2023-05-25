import logging

# Base class for table definitions.
from dls_normsql.table_definition import TableDefinition

from soakdb3_api.databases.constants import (
    BodyFieldnames,
    HeadFieldnames,
    Tablenames,
    VisitFieldnames,
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class HeadTable(TableDefinition):
    # ----------------------------------------------------------------------------------------
    def __init__(self):
        TableDefinition.__init__(self, Tablenames.HEAD)

        self.fields[HeadFieldnames.Version] = {"type": "REAL"}
        self.fields[HeadFieldnames.LabVisit] = {"type": "TEXT"}
        self.fields[HeadFieldnames.Path] = {"type": "TEXT"}
        self.fields[HeadFieldnames.Protein] = {"type": "TEXT"}
        self.fields[HeadFieldnames.DropVolume] = {"type": "REAL"}
        self.fields[HeadFieldnames.CrystalsPerBatch] = {"type": "INTEGER"}
        self.fields[HeadFieldnames.OneBatchPerPlate] = {"type": "TEXT"}
        self.fields[HeadFieldnames.CompoundStock] = {"type": "REAL"}
        self.fields[HeadFieldnames.SolventPercent] = {"type": "REAL"}
        self.fields[HeadFieldnames.CryoStock] = {"type": "REAL"}
        self.fields[HeadFieldnames.DesiredCryo] = {"type": "REAL"}
        self.fields[HeadFieldnames.CryoLocation] = {"type": "TEXT"}
        self.fields[HeadFieldnames.DesiredSoakTime] = {"type": "REAL"}
        self.fields[HeadFieldnames.CrystalStartNumber] = {"type": "INTEGER"}
        self.fields[HeadFieldnames.BeamlineVisit] = {"type": "TEXT"}
        self.fields[HeadFieldnames.SpaceGroup] = {"type": "TEXT"}
        self.fields[HeadFieldnames.A] = {"type": "REAL"}
        self.fields[HeadFieldnames.B] = {"type": "REAL"}
        self.fields[HeadFieldnames.C] = {"type": "REAL"}
        self.fields[HeadFieldnames.alpha] = {"type": "REAL"}
        self.fields[HeadFieldnames.beta] = {"type": "REAL"}
        self.fields[HeadFieldnames.gamma] = {"type": "REAL"}
        self.fields[HeadFieldnames.Recipe] = {"type": "TEXT"}
        self.fields[HeadFieldnames.Resolution] = {"type": "REAL"}
        self.fields[HeadFieldnames.CentringMethod] = {"type": "TEXT"}
        self.fields[HeadFieldnames.EUBOpen] = {"type": "TEXT"}
        self.fields[HeadFieldnames.iNEXT] = {"type": "TEXT"}
        self.fields[HeadFieldnames.Covid19] = {"type": "TEXT"}
        self.fields[HeadFieldnames.ILOXchem] = {"type": "TEXT"}


# ----------------------------------------------------------------------------------------
class BodyTable(TableDefinition):
    # ----------------------------------------------------------------------------------------
    def __init__(self):
        TableDefinition.__init__(self, Tablenames.BODY)

        self.fields[BodyFieldnames.ID] = {
            "type": "INTEGER PRIMARY KEY",
            "index": True,
        }
        self.fields[BodyFieldnames.LabVisit] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.LibraryPlate] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.SourceWell] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.LibraryName] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CompoundSMILES] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CompoundCode] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CrystalPlate] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CrystalWell] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.EchoX] = {"type": "INTEGER"}
        self.fields[BodyFieldnames.EchoY] = {"type": "INTEGER"}
        self.fields[BodyFieldnames.DropVolume] = {"type": "REAL"}
        self.fields[BodyFieldnames.ProteinName] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.BatchNumber] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CompoundStockConcentration] = {"type": "REAL"}
        self.fields[BodyFieldnames.CompoundConcentration] = {"type": "REAL"}
        self.fields[BodyFieldnames.SolventFraction] = {"type": "REAL"}
        self.fields[BodyFieldnames.SoakTransferVol] = {"type": "REAL"}
        self.fields[BodyFieldnames.SoakStatus] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.SoakTimestamp] = {"type": "UNKNOWN"}
        self.fields[BodyFieldnames.CryoStockFraction] = {"type": "REAL"}
        self.fields[BodyFieldnames.CryoFraction] = {"type": "REAL"}
        self.fields[BodyFieldnames.CryoWell] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CryoTransferVolume] = {"type": "REAL"}
        self.fields[BodyFieldnames.CryoStatus] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CryoTimestamp] = {"type": "UNKNOWN"}
        self.fields[BodyFieldnames.SoakingTime] = {"type": "REAL"}
        self.fields[BodyFieldnames.HarvestStatus] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.CrystalName] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.Puck] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.PuckPosition] = {"type": "INTEGER"}
        self.fields[BodyFieldnames.PinBarcode] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.MountingResult] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.MountingArrivalTime] = {"type": "UNKNOWN"}
        self.fields[BodyFieldnames.MountedTimestamp] = {"type": "UNKNOWN"}
        self.fields[BodyFieldnames.MountingTime] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.ispybStatus] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.DataCollectionVisit] = {"type": "VARCHAR"}
        self.fields[BodyFieldnames.SoakDBComments] = {"type": "TEXT"}


# ----------------------------------------------------------------------------------------
class VisitTable(TableDefinition):
    # ----------------------------------------------------------------------------------------
    def __init__(self):
        TableDefinition.__init__(self, Tablenames.VISIT)

        self.fields[VisitFieldnames.VISITID] = {"type": "VARCHAR"}
