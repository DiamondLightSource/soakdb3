PWD = $(shell pwd)
whoami = $(shell whoami)
VERSION = 0.0.15
VERBOSE ?= 

# ------------------------------------------------------------------
# Set up path local clone of dependencies supercede the installed ones.
# The paths should be absolute since tasks can be launched in their own working directories.
SRC_PATH=$(PWD)/src
BASIC_PATH=/22/dls-utilpack/src:/22/dls-normsql/src:/22/dls-siggy/src:/22/dls-logformatter/src
BILLY_PATH=/22/soakdb3/src
MAINIAC_PATH=/22/dls-mainiac/src
VALKYRIE_PATH=/22/dls-pairstream/src
PYTHONPATH=$(SRC_PATH):$(BASIC_PATH):$(BILLY_PATH):$(MAINIAC_PATH):$(VALKYRIE_PATH)

ISPYB_LOCAL_CREDENTIALS = ispyb-local.cfg
ISPYB_RO_CREDENTIALS = ispyb-ro.cfg

# To set the PYTHONPATH in your shell, use this command: export PYTHONPATH=`make pythonpath`
pythonpath:
	@echo $(PYTHONPATH)

pytest:
	PYTHONPATH=$(PYTHONPATH) \
	ISPYB_CREDENTIALS=$(ISPYB_LOCAL_CREDENTIALS) \
	python3 -m pytest

# ------------------------------------------------------------------
# Tests individually (lib)

test:
	PYTHONPATH=tests:$(PYTHONPATH) \
	AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS=tests.infrastructures.airflow_logging_config.LOGGING_CONFIG_DICT \
	ISPYB_CREDENTIALS=$(ISPYB_LOCAL_CREDENTIALS) \
	python3 -m pytest -sv -ra --tb=line tests/$(t)

	
# ------------------------------------------------------------------
# Docker containers.
CCP4_CONTAINER = /scratch/$(whoami)/ccp4_container
copy_ccp4_container:
	mkdir -p $(CCP4_CONTAINER)
	rsync -a /dls_sw/apps/ccp4/7.1.018/* $(CCP4_CONTAINER)

build_ccp4_container:
	cp -rdpa docker/ccp4/* $(CCP4_CONTAINER)
	cd $(CCP4_CONTAINER) && podman build . -t ccp4-7.1

XCE_CONTAINER = /scratch/$(whoami)/xce_container
build_xce_container:
	mkdir -p $(XCE_CONTAINER)
	rsync -a --exclude "*/.git" ../XChemExplorer $(XCE_CONTAINER)
	cp -rdpa docker/xce/* $(XCE_CONTAINER)
	cd $(XCE_CONTAINER) && podman build . -t xchem_explorer

	
# ------------------------------------------------------------------
service = dataface

start:
	PYTHONPATH=$(PYTHONPATH) \
	SOAKDB_CONFIGFILE=configurations/multibox.yaml \
	python3 -m soakdb3_cli.main start_services $(service) \
	$(V)
	
# ------------------------------------------------------------------
# Rsync.

rsync:	
	../kbp43231_scripts/myrsync.py xchem-be

rsync_xce:	
	../kbp43231_scripts/myrsync.py XChemExplorer

copy:	
	bash -c "../kbp43231_scripts/mycopy.py c:/22/dls-xchem_be/Makefile"

# ------------------------------------------------------------------
# Utility.

tree:
	tree -I "__*" soakdb3_cli

	tree -I "__*" tests

.PHONY: list
list:
	@awk "/^[^\t:]+[:]/" Makefile | grep -v ".PHONY"

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -rf {} \;

show_version:
	PYTHONPATH=$(PYTHONPATH) python3 src/soakdb3_lib/version.py --json
	PYTHONPATH=$(PYTHONPATH) python3 src/soakdb3_lib/version.py

# ------------------------------------------------------------------
# Version bumping.  Configured in setup.cfg. 
# Thanks: https://pypi.org/project/bump2version/
bump-patch:
	bump2version --list patch

bump-minor:
	bump2version --list minor

bump-major:
	bump2version --list major
	
bump-dryrun:
	bump2version --dry-run patch

# Saved 44

