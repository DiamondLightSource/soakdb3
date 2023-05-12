:: This file starts the soakdb3 excel frontend.
:: It must be copied to the visit directory and run from there.

set SOAKDB3_VISITID=%~dp0..
set SOAKDB3_CONFIGFILE=\\dc\dls_sw\apps\xchem\xchem-lifesupport\configurations\soakdb3_production.json
start excel /x "\\dc\dls_sw\apps\xchem\soakdb3\spreadsheets\1.3.0\soakDB_v3.0.xlsm"
