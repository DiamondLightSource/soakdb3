Building the conda environment
=======================================================================

The production backend is built as a conda environment.

Install the soakdb3 package in a virtual environment::

    $ module load python/3.10
    $ python3 -m venv /scratch/$USER/soakdb3
    $ source /scratch/$USER/soakdb3/bin/activate
    $ pip install --upgrade pip
    $ pip install soakdb3

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

Make this the edge version::

    $ make edge_conda

Or the stable version::

    $ make stable_conda
