# Nexus Gateway Docs — Course Companion

This is the demo project for the course  
**Professional Localization with Sphinx, Poedit & Read the Docs**.

Follow the steps below to get the project running on your machine before 
following along with the video.

---

## Prerequisites

- **Python 3.9 or later** — [python.org/downloads](https://www.python.org/downloads/)
- **Poedit** (free version is sufficient for the course) — [poedit.com](https://poedit.com)
- **Git** — [git-scm.com](https://git-scm.com)· the project should be initialised as a repository and connected to a remote on GitHub before reaching the Read the Docs section.
- A terminal (Command Prompt, PowerShell, or any shell on macOS/Linux)
- Basic familiarity with the command line

No prior Sphinx experience is required to follow the localization workflow, 
but knowing what Sphinx is and what it produces will help. If you are 
completely new to Sphinx, the official 
[Sphinx Getting Started guide](https://www.sphinx-doc.org/en/master/usage/quickstart.html) 
is a good 15-minute primer before starting this course.

---

## Step 1 — Verify Your Python Installation

Open a terminal and run:

```
python --version
```

or on some systems:

```
python3 --version
```

You should see `Python 3.9.x` or later. If Python is not installed, 
download it from [python.org](https://www.python.org/downloads/) and 
run the installer. On Windows, check **Add Python to PATH** during installation.

---

## Step 2 — Create a Virtual Environment

Before installing any packages, create a virtual environment for this 
project. This keeps the project's dependencies isolated from your global 
Python installation and avoids version conflicts with other projects.

Navigate to the `nexus-gateway-docs` folder and run:

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should now show `(.venv)` at the start, confirming 
the virtual environment is active.

> **Note:** You need to activate the virtual environment every time you 
> open a new terminal session to work on this project. Just run the 
> `activate` command above again — you do not need to recreate the 
> environment.

---

## Step 3 — Install the Required Tools

With the virtual environment active, install Sphinx, the sphinx-intl 
localization tool, and the Furo theme used by this project:

```
pip install sphinx sphinx-intl furo
```

Verify the installations:

```
sphinx-build --version
pip show sphinx-intl
```

Both commands should return a version number without errors.

---

## Step 4 — Extract and Open the Project

Extract the downloaded archive. You will get a folder called 
`nexus-gateway-docs` with the following structure:

```
nexus-gateway-docs/
├── README.md                  ← you are here
└── docs/
    └── source/
        ├── conf.py            ← Sphinx configuration
        ├── index.rst          ← root document
        ├── _static/
        │   └── architecture.png
        ├── _templates/
        │   └── layout.html    ← custom Jinja template
        ├── concepts/
        │   ├── what-is-nexus-gateway.rst
        │   ├── authentication.rst
        │   ├── rate-limiting.rst
        │   └── routing.rst
        └── guides/
            ├── getting-started.rst
            └── configuring-routes.rst
```

---

## Step 5 — Do a First English Build

Navigate into the `docs` directory:

```
cd nexus-gateway-docs/docs
```

Build the English version to verify everything is working:

```
sphinx-build -b html source build/html
```

Sphinx will create a `build/` folder and output the HTML docs inside it. 
Open `build/html/index.html` in your browser. You should see the 
Nexus Gateway documentation site in English.

If the build completes with **build succeeded** and no errors, you are 
ready to follow along with the course.

---

## Step 6 — Ready to Start

Once the English build works, you are at exactly the same starting point 
as the course video. Everything from this point is covered in the video.

For reference, here is the complete localization workflow you will follow:

### Extract gettext strings

```
sphinx-build -b gettext source build/gettext
```

### Generate French .po files

```
sphinx-intl update -p ./build/gettext -l fr
```

### Translate in Poedit

Open the `.po` files from `source/locale/fr/LC_MESSAGES/` in Poedit and translate each folder's strings — `concepts.po` covers all concept pages, `guides.po` covers all guide pages.

### Build the French docs locally

```
sphinx-autobuild -a -D language=en source build/html/fr
```

Open `build/html/fr/index.html` in your browser to review the translation.

### Rebuild after source changes

When the English source files change, re-run the extraction and update 
steps to pick up new strings, then translate the new entries in Poedit:

```
sphinx-build -b gettext source build/gettext
sphinx-intl update -p ./build/gettext -l fr
```

---

## What Is in This Project

The Nexus Gateway project is a fictional API gateway product. The 
documentation is realistic enough to serve as a professional localization 
exercise, covering a range of content types:

- **Conceptual documentation** — explanations, lists, tables, notes, warnings
- **Step-by-step guides** — numbered procedures, code blocks, cross-references
- **Custom Jinja template** — footer and sidebar strings wrapped in `_()` 
  for gettext extraction
- **Localizable image** — `architecture.png` can have a French version 
  as `architecture.fr.png` to demonstrate the `figure_language_filename` setting

---

## Useful Links

- [Sphinx Internationalization](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [sphinx-intl documentation](https://sphinx-intl.readthedocs.io/)
- [Poedit documentation](https://poedit.com/docs/)
- [Read the Docs — Localization guide](https://docs.readthedocs.com/platform/stable/localization.html)
