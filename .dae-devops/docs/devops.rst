.. # ********** Please don't edit this file!
.. # ********** It has been generated automatically by dae_devops version 0.5.2.
.. # ********** For repository_name soakdb3

Devops
=======================================================================

There exists a a configuration file called ``.dae-devops/project.yaml``.

This file defines the project information needed for CI/CD.

It is parsed by the ``dae_devops.force`` command which creates these files:

- pyproject.toml
- .gitlab-ci.yml
- .dae-devops/Makefile
- .dae-devops/docs/*

Local CI/CD execution
-----------------------------------------------------------------------

All the CI/CD ops which are run by the git server can be run at the command line.

Running these ops before pushing to the git server can make the turnaround quicker to fix things.

Follow the steps in the Developing section.  Then you can run the following commands.

Validation of the code::

    $ make -f .dae-devops/Makefile validate_pre_commit
    $ make -f .dae-devops/Makefile validate_mypy
    $ make -f .dae-devops/Makefile validate_pytest
    $ make -f .dae-devops/Makefile validate_docs

Packaging:: 

    $ make -f .dae-devops/Makefile package_pip

Publishing::

    $ make -f .dae-devops/Makefile publish_pip
    $ make -f .dae-devops/Makefile publish_docs
    


.. # dae_devops_fingerprint f77696d690fbd428333796c0bf2f67df
