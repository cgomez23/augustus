"""Sphinx configuration."""
project = "augustus"
author = "Carlos Gomez"
copyright = "2024, Carlos Gomez"
extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.coverage', 
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
