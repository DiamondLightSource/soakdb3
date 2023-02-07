
Starting Backend Services
=======================================================================

The production Soakdb3 backend is implemented as set of services. 
They need to be started before you can run the Excel spreadsheet frontends.

Only one instance of the service needs to be started for all visits.

The beamline staff should start the services, not a visitor user.

Start the services::

    $ ssh i04-1-ws004
    $ module load xchem/soakdb3/stable
    $ soakdb3_start

You should leave the services running in the console window.
You can stop them any time by typing ^C. 
