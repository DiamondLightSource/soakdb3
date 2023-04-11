# ********** Please don't edit this file!
# ********** It has been generated automatically by dae_devops version 0.5.2.
# ********** For repository_name soakdb3

from pathlib import Path
from subprocess import check_output

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from sphinx.domains.python import PythonDomain

import soakdb3_lib

# -- General configuration ------------------------------------------------

# General information about the project.
project = "soakdb3"

# The full version, including alpha/beta/rc tags.
release = soakdb3_lib.__version__

# The short X.Y version.
if "+" in release:
    # Not on a tag, use branch name
    root = Path(__file__).absolute().parent.parent
    git_branch = check_output("git branch --show-current".split(), cwd=root)
    version = git_branch.decode().strip()
else:
    version = release

extensions = [
    # Use this for generating API docs
    "sphinx.ext.autodoc",
    # This can parse google style docstrings
    "sphinx.ext.napoleon",
    # For linking to external sphinx documentation
    "sphinx.ext.intersphinx",
    # Add links to source code in API docs
    "sphinx.ext.viewcode",
    # Adds the inheritance-diagram generation directive
    "sphinx.ext.inheritance_diagram",
    # Add a copy button to each code block
    "sphinx_copybutton",
    # For the card element
    "sphinx_design",
    # For command line tools autodoc.
    "sphinxarg.ext",
    # Create pages from jupyter notebooks
    "nbsphinx",
    "IPython.sphinxext.ipython_console_highlighting",
]

# If true, Sphinx will warn about all references where the target cannot
# be found.
nitpicky = True

# A list of (type, target) tuples (by default empty) that should be ignored when
# generating warnings in "nitpicky mode". Note that type should include the
# domain name if present. Example entries would be ('py:func', 'int') or
# ('envvar', 'LD_LIBRARY_PATH').
nitpick_ignore = [("py:class", "numpy.ma.core.MaskedArray")]

# Workaround for NewType as autodata, to be removed when issue is resolved
# see: https://github.com/sphinx-doc/sphinx/issues/9560
assert PythonDomain.object_types["data"].roles == ("data", "obj")
PythonDomain.object_types["data"].roles = ("data", "class", "obj")
# Both the class’ and the __init__ method’s docstring are concatenated and
# inserted into the main body of the autoclass directive
autoclass_content = "both"

# Order the members by the order they appear in the source code
autodoc_member_order = "bysource"

# Don't inherit docstrings from baseclasses
autodoc_inherit_docstrings = False

# Don't show the typehints in the function/method signature.
autodoc_typehints = "description"

# Output graphviz directive produced images in a scalable format
graphviz_output_format = "svg"

# The name of a reST role (builtin or Sphinx extension) to use as the default
# role, that is, for text marked up `like this`
default_role = "any"

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# This means you can link things like `str` and `asyncio` to the relevant
# docs in the python documentation.
intersphinx_mapping = dict(
    python=("https://docs.python.org/3/", None),
    numpy=("https://numpy.org/doc/stable/", None),
)

# A dictionary of graphviz graph attributes for inheritance diagrams.
inheritance_graph_attrs = dict(rankdir="TB")

# Common links that should be available on every page
rst_epilog = """
.. _Diamond Light Source: http://www.diamond.ac.uk
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _mypy: http://mypy-lang.org/
.. _pre-commit: https://pre-commit.com/
"""

# Ignore localhost links for periodic check that links in docs are valid
linkcheck_ignore = [r"http://localhost:\d+/"]

# Set copy-button to ignore python and bash prompts
# https://sphinx-copybutton.readthedocs.io/en/latest/use.html#using-regexp-prompt-identifiers
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# These folders are copied to the documentation's HTML output
html_static_path = ["_static"]

# Paths are either relative to html_static_path or fully qualified paths (eg. https://...)
html_css_files = [
    # Custom css to allow use of full window width in the browser.
    "css/custom.css",
]

# Theme options for pydata_sphinx_theme
html_theme_options = dict(
    logo=dict(
        text=project,
    ),
    gitlab_url="None/soakdb3",
    icon_links=[],
    navbar_end=["theme-switcher", "icon-links"],
)

# A dictionary of values to pass into the template engine’s context for all pages
html_context = dict(
    doc_path="docs",
)

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# Disable the link to show the rst source.
# I did this since it's noise on the page and most audience doesn't care to see the raw rst.
html_show_sourcelink = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# Logo
html_logo = "images/dls-logo.svg"
html_favicon = "images/dls-favicon.ico"


def ultimateReplace(app, docname, source):
    result = source[0]
    for key in app.config.ultimate_replacements:
        result = result.replace(key, app.config.ultimate_replacements[key])
    source[0] = result


# I got this from https://github.com/sphinx-doc/sphinx/issues/4054.
# It will allow the ${token} replacement in the rst documents.
ultimate_replacements = {
    "$" + "{repository_name}": "soakdb3",
    "$" + "{package_name}": "soakdb3_lib",
    "$" + "{git_url}": "None",
    "$" + "{python_version_at_least}": "3.1",
}


def setup(app):
    app.add_config_value("ultimate_replacements", {}, True)
    app.connect("source-read", ultimateReplace)


# dae_devops_fingerprint 2b0bd1b9aacaccb81e02f6c3ba44a437
