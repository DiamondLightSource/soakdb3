Building the conda environment
=======================================================================

The production backend is built as a conda environment.

Install the soakdb3 package in a virtual environment::

    $ module load python/3.10
    $ python3 -m venv /scratch/$USER/venv/soakdb3
    $ source /scratch/$USER/venv/soakdb3/bin/activate
    $ pip install --upgrade pip
    $ pip install --upgrade soakdb3

Make sure you have the version of soakdb3 you expect, since this is the version used to name the conda environment::

    $ soakdb3 --version

Get to the Makefile containing the commands to build the conda environment::

    $ git clone https://gitlab.diamond.ac.uk/xchem/soakdb3_configuration.git
    $ cd soakdb3_configuration

Or, you can use the production soakdb3 configuration::

    $ cd /dls_sw/apps/xchem/soakdb3/soakdb3_configuration

Build and provision the conda environment::

    $ make create_conda
    $ make provision_conda

Change the version in the modulefile::

    $ vi /dls_sw/apps/xchem/soakdb3/soakdb3_configuration/modulefile    
      (change the line starting with: set conda_environment_version)
    
Make this the edge version::

    $ make deploy_modules
    $ make deploy_spreadsheets

And, if you wish, the stable version::

    $ make deploy_modules_stable
    $ make deploy_spreadsheets_stable

Check you have the right version by starting a new shell and::

    $ module load xchem/soakdb3/stable

Follow the instructions for starting the backend and for starting the frontend.
