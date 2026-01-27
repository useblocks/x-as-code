# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
from pathlib import Path

import jinja2

# We need to make Python aware of our project source code, which is stored outside `/docs`,
# under `src/`
code_path = os.path.join(os.path.dirname(__file__), "../", "./")
sys.path.append(code_path)
print(f"CODE_PATH: {code_path}")


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "X as Code (XaC)"
copyright = "2026, team useblocks"
author = "team useblocks and friends"
version = "1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# List of Sphinx extension to use.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_needs",
    "sphinx_design",
    "sphinxcontrib.plantuml",
    "sphinx_simplepdf",
    "sphinx_codelinks",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.test_reports",
]

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "needs": ("https://sphinx-needs.readthedocs.io/en/latest/", None),
}

###############################################################################
# SPHINX-NEEDS Config START
###############################################################################

# Read the configuration from an external TOML file.
# This makes it possible to use ubCode and its tools directly with
# the project. Declarative configuration formats are also preferred as they
# cannot contain logic and can be consumed by almost all languages.
needs_from_toml = "ubproject.toml"

needs_string_links = {
    # Adds link to the Sphinx-Needs configuration page
    'config_link': {
        'regex': r'^(?P<value>.*)$',
        'link_url': '{{value}}',
        'link_name': 'GitHub',
        'options': ['url']
    },
}

src_trace_config_from_toml = "src_trace.toml"

###############################################################################
# SPHINX-NEEDS Config END
###############################################################################

###############################################################################
# SPHINX-TEST-REPORTS Config START
###############################################################################

tr_rootdir = Path("src")
tr_file_option = "test_file"

###############################################################################
# SPHINX-TEST-REPORTS Config END
###############################################################################

###############################################################################
# Mermaid Config START
###############################################################################

mermaid_params = ['--theme', 'forest', '--backgroundColor', 'transparent']

###############################################################################
# Mermaid Config END
###############################################################################

templates_path = ["_templates"]

# List of files/folder to ignore.
# Sphinx builds all ``.rst`` files under ``/docs``, no matte if they are part
# of a toctree or not. So as we have some rst-templates, we need to tell Sphinx to ignore
# these files.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    ".ub_cache",
    "_build"
]

# We bring our own plantuml jar file.
# These options tell Sphinxcontrib-PlantUML we it can find this file.
local_plantuml_path = os.path.join(
    os.path.dirname(__file__), "utils", "plantuml-1.2022.14.jar"
)
plantuml = f"java -Djava.awt.headless=true -jar {local_plantuml_path}"
# plantuml_output_format = 'png'
plantuml_output_format = "svg_img"

supress_warnings = ["needs.mistyped_external_values",
                    "needs.config"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": True,
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/useblocks/x-as-code",
    "source_branch": "main",
    "source_directory": "docs",
    "light_logo": "xac_logo.png",
    "dark_logo": "xac_logo_dark.png",
}
html_css_files = ["custom.css"]
