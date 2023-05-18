# ----------------------------------------------------------------------------------------
class Tablenames:
    HEAD = "soakdb"
    BODY = "mainTable"
    VISIT = "visit"


# ----------------------------------------------------------------------------------------
class HeadFieldnames:
    Version = "Version"
    LabVisit = "LabVisit"
    Path = "Path"
    Protein = "Protein"
    DropVolume = "DropVolume"
    CrystalsPerBatch = "CrystalsPerBatch"
    OneBatchPerPlate = "OneBatchPerPlate"
    CompoundStock = "CompoundStock"
    SolventPercent = "SolventPercent"
    CryoStock = "CryoStock"
    DesiredCryo = "DesiredCryo"
    CryoLocation = "CryoLocation"
    DesiredSoakTime = "DesiredSoakTime"
    CrystalStartNumber = "CrystalStartNumber"
    BeamlineVisit = "BeamlineVisit"
    SpaceGroup = "SpaceGroup"
    A = "A"
    B = "B"
    C = "C"
    alpha = "alpha"
    beta = "beta"
    gamma = "gamma"
    Recipe = "Recipe"
    Resolution = "Resolution"
    CentringMethod = "CentringMethod"
    EUBOpen = "EUBOpen"
    iNEXT = "iNEXT"
    Covid19 = "Covid19"
    ILOXchem = "ILOXchem"


# ----------------------------------------------------------------------------------------
class BodyFieldnames:
    ID = "ID"
    LabVisit = "LabVisit"
    LibraryPlate = "LibraryPlate"
    SourceWell = "SourceWell"
    LibraryName = "LibraryName"
    CompoundSMILES = "CompoundSMILES"
    CompoundCode = "CompoundCode"
    CrystalPlate = "CrystalPlate"
    CrystalWell = "CrystalWell"
    EchoX = "EchoX"
    EchoY = "EchoY"
    DropVolume = "DropVolume"
    ProteinName = "ProteinName"
    BatchNumber = "BatchNumber"
    CompoundStockConcentration = "CompoundStockConcentration"
    CompoundConcentration = "CompoundConcentration"
    SolventFraction = "SolventFraction"
    SoakTransferVol = "SoakTransferVol"
    SoakStatus = "SoakStatus"
    SoakTimestamp = "SoakTimestamp"
    CryoStockFraction = "CryoStockFraction"
    CryoFraction = "CryoFraction"
    CryoWell = "CryoWell"
    CryoTransferVolume = "CryoTransferVolume"
    CryoStatus = "CryoStatus"
    CryoTimestamp = "CryoTimestamp"
    SoakingTime = "SoakingTime"
    HarvestStatus = "HarvestStatus"
    CrystalName = "CrystalName"
    Puck = "Puck"
    PuckPosition = "PuckPosition"
    PinBarcode = "PinBarcode"
    MountingResult = "MountingResult"
    MountingArrivalTime = "MountingArrivalTime"
    MountedTimestamp = "MountedTimestamp"
    MountingTime = "MountingTime"
    ispybStatus = "ispybStatus"
    DataCollectionVisit = "DataCollectionVisit"
    SoakDBComments = "SoakDBComments"


# ----------------------------------------------------------------------------------------
# Constants used in the PinBarcode field when something goes wrong.
# These would get written into the spreadsheet Pin Barcode column.
# We decided to go back to blank values since these get exported to ispyb and read by the beamline,
# and it's possible anything other than a barcode or -CANT-FIND- might mess up the scanning robot.
# The code writes logger.warning with the [ANOMALY] tag containing details.
class PinBarcodeErrors:
    NO_PUCK = ""
    BAD_PIN = ""
    BAD_INT = ""
    BAD_DATE = ""
    CANT_FIND = "-CANT-FIND-"


# ----------------------------------------------------------------------------------------
class VisitFieldnames:
    CREATED_ON = "created_on"
    VISITID = "visitid"
