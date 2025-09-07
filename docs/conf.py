# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Smooth Criminal'
copyright = '2025, Adolfo González'
author = 'Adolfo González'

version = '0.5.0'
release = '0.5.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'numpydoc',
]

autodoc_mock_imports = [
    'numba',
    'numpy',
    'pandas',
    'flet',
    'tabulate',
    'matplotlib',
    'openpyxl',
    'tinydb',
    'playsound',
    'rich',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
