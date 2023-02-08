
Starting Service (Development)
=======================================================================

The Soakdb3 backend is implemented as set of services. 
They need to be started before you can run the Excel spreadsheet frontend.

Please follow the steps from the Installing section.

You will need a configuration.  A ready example is provided in the source code.
You can clone the source code by::

    $ git clone ${git_url}/${repository_name}.git
    $ cd ${repository_name}

Start the services::

    $ soakdb3.cli start_services \
    $   --configuration=configurations/multibox.yaml \
    $   --visit=lb19758-64 \
    $   --visit_directory=/dls/labxchem/data/lb19758/lb19758-64

You should see some lines of output including something like::

    soakdb3_lib.databases.aiosqlite.Aiosqlite database file is /dls/labxchem/data/lb19758/lb19758-64/processing/database/soakDBDataFile.sqlite revision 1

You should leave the services running int he console window.
You can stop them any time by typing ^C. 

|

Now you need to get a copy of the excel spreadsheet and auxiliary files.  Do the following commands on a Windows computer::

    $ copy/r \\cs04r-nas02-05.diamond.ac.uk\dls_sw\apps\xchem\conda\envs\soakdb3\stable\lib\python3.10\site-packages\soakdb3_xls\* Y:\labxchem\data\lb19758\lb19758-64\processing\lab36


You will need to edit the excel configuration file to point
to the hostname of the Linux computer where you started the services::

    $ edit configuration.json
    $ change the hostname and save the file:

Finally, you can start the spreadsheet::
    
    $ soakDB3.bat
