# ********** Please don't edit this file!
# ********** It has been generated automatically by dae_devops version 0.5.2.
# ********** For repository_name soakdb3

# ---------------------------------------------------------------------
# These make targets are designed to be called from the command line and from .gitlab-ci.yml.
# ---------------------------------------------------------------------

# I put the package_pip artifacts int this place for now until I can use the corporate internal pipserver.
# Maybe /dls_sw/work/python3/RHEL7-x86_64/distributions would be a better place?
PIP_FIND_LINKS = /dls_sw/apps/bxflow/artifacts

# I got these from https://gitlab.diamond.ac.uk/controls/reports/ci_templates/-/blob/master/defaults.yml.
# Directory where docs are published.
DOCS_PUBLISH_ROOT = /dls/cs-www/reports/gitlab-ci/soakdb3

# ---------------------------------------------------------------------
# These are called from the default before_script in the gitlab CI.
# That meants it is normally called before any other job.
# It installs things not covered by pyproject.toml.

prepare_git_dependencies:
	chmod a+x .dae-devops/prepare_git_dependencies.sh
	.dae-devops/prepare_git_dependencies.sh

# ---------------------------------------------------------------------
# The validate stage makes sure code is ready to package and release.

validate: \
	validate_pre_commit \
	validate_mypy \
	validate_pytest
	echo "validation complete"
	
validate_pre_commit: 
	tox -q -e pre-commit

validate_mypy: 
	tox -q -e mypy

validate_pytest: 
	tox -q -e pytest

validate_docs: 
	tox -q -e docs

# ---------------------------------------------------------------------
# The pip state packages and publishes for pip.

package: \
	package_pip

package_pip:
	pip install pipx twine
	pipx run build

# ---------------------------------------------------------------------
# The publish stage publishes things which have already been built or packaged.

publish: \
	publish_pip \
	publish_docs

publish_pip:
	cp -v -p dist/*.whl $(PIP_FIND_LINKS)

publish_docs:
	mkdir -p $(DOCS_PUBLISH_ROOT)
	cp -r build/html/* $(DOCS_PUBLISH_ROOT)
	

# dae_devops_fingerprint 17444c38bc0036a20fb9a2d8c598b25b
