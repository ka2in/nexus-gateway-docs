# Configuration file for the Sphinx documentation builder.
# Nexus Gateway Documentation

project = "Nexus Gateway"
copyright = "2026, Nexus Technologies"
author = "Nexus Technologies Documentation Team"
release = "2.4"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

# -- Localized images --------------------------------------------------------
# Sphinx will look for language-specific images using this pattern.
# For example: architecture.fr.png for the French version.

figure_language_filename = "{root}.{language}{ext}"

# -- HTML output -------------------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": False,
}
