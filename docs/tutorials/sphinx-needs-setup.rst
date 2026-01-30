.. _tutorial-sphinx-needs-setup:

:octicon:`rocket` Setting Up a Sphinx-Needs Project
===================================================

This tutorial guides you through setting up a new Sphinx documentation
project with sphinx-needs from scratch. By the end, you'll have a
working documentation system that can manage requirements,
specifications, and traceability.

.. note::

   **Target audience**: Software developers (especially C++ developers)
   who are new to Sphinx but want to leverage documentation-as-code for
   requirements management.

Prerequisites
-------------

Before starting, ensure you have:

* **Python 3.12+** installed on your system (required by Sphinx 9.x and
  sphinx-needs 6.x)
* **uv** - a fast Python package and project manager
* A terminal/command line
* A text editor or IDE (VS Code with ubCode extension recommended)

.. note::

   **Version Compatibility:**

   * Sphinx 9.x requires Python 3.12 or higher
   * sphinx-needs 6.x requires Sphinx 7.4+ and Python 3.10+
   * For best results, use the latest stable versions of both

If you don't have ``uv`` installed, install it first:

.. code-block:: bash

   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

.. tip::

   **What is uv?**

   uv is an extremely fast Python package and project manager written in
   Rust. It's 10-100x faster than pip and replaces pip, virtualenv, and
   pyenv in a single tool. It handles virtual environments, dependencies,
   and Python version management seamlessly.

What is Sphinx?
---------------

If you're coming from a C++ background, you might be familiar with
Doxygen for code documentation. Sphinx is similar but more powerful:

* **Sphinx** is a documentation generator that converts reStructuredText
  (or Markdown) files into HTML, PDF, and other formats
* **reStructuredText (RST)** is a lightweight markup language (like
  Markdown, but with more features for technical documentation)
* **sphinx-needs** is a Sphinx extension that adds requirements
  management capabilities

Think of it as: **RST files → Sphinx → Beautiful HTML documentation**

The Sphinx-Needs Advantage
~~~~~~~~~~~~~~~~~~~~~~~~~~

For C++ developers, the key advantages over Doxygen are:

1. **Requirements as Code**: Define requirements, specifications, and
   test cases directly in your documentation
2. **Traceability**: Automatic linking between requirements → specs →
   tests → implementation
3. **Visualization**: Generate flow diagrams, tables, and matrices
   showing relationships
4. **Export**: Generate ``needs.json`` for integration with other tools
5. **Validation**: Enforce ID formats, required fields, and constraints

How Sphinx-Needs Works
~~~~~~~~~~~~~~~~~~~~~~

Sphinx-needs manages "need items" through a lifecycle:

1. **Collection**: Needs are parsed from RST files during the read phase
2. **Resolution**: Dynamic fields and links are resolved
3. **Analysis**: Directives like ``needtable`` and ``needflow`` query the
   collected needs
4. **Rendering**: Needs are rendered to HTML, PDF, or other formats
5. **Validation**: Constraints and warnings are checked

Each need is a node in a graph structure with:

* A **type** (requirement, specification, test, etc.)
* A unique **ID** for traceability
* A **title** and **description**
* Optional **metadata** (status, tags, priority, etc.)
* **Links** to other needs

.. seealso:: For comprehensive documentation, see the `official sphinx-needs website <https://sphinx-needs.readthedocs.io/en/latest/>`_.

Step 1: Create Project Directory
--------------------------------

Create a new directory for your documentation project:

.. code-block:: bash

   mkdir my-docs-project
   cd my-docs-project

Step 2: Set Up Python Environment with uv
-----------------------------------------

Initialize a new Python project with uv:

.. code-block:: bash

   # Initialize project with Python 3.12
   uv init --python 3.12

   # Create virtual environment (uv manages this automatically)
   uv venv

   # On macOS/Linux, activate it:
   source .venv/bin/activate

   # On Windows:
   # .venv\Scripts\activate

Your project structure now looks like:

.. code-block:: text

   my-docs-project/
   ├── .venv/
   ├── .python-version
   ├── pyproject.toml
   └── hello.py            # You can delete this

.. note::

   With uv, you can also run commands directly without activating the
   virtual environment by prefixing them with ``uv run``. This is the
   recommended approach as it ensures the correct environment is always
   used.

Step 3: Install Dependencies
----------------------------

Add Sphinx and sphinx-needs to your project:

.. code-block:: bash

   uv add sphinx==8.3.0 sphinx-needs==6.3.0

This installs:

* **Sphinx 8.3.0** - The documentation generator
* **sphinx-needs 6.3.0** - Requirements management extension

.. tip::

   You can verify the installation with:

   .. code-block:: bash

      uv run sphinx-build --version
      # Output: sphinx-build 8.3.0

Step 4: Initialize Sphinx Project
---------------------------------

Run the Sphinx quickstart wizard. This creates a source directory and
generates a default ``conf.py`` with useful configuration values:

.. code-block:: bash

   uv run sphinx-quickstart docs

Answer the prompts as follows:

.. code-block:: text

   > Separate source and build directories (y/n) [n]: n
   > Project name: My Documentation Project
   > Author name(s): Your Name
   > Project release []: 0.1.0
   > Project language [en]: en

This creates the following structure:

.. code-block:: text

   my-docs-project/
   ├── docs/
   │   ├── conf.py          # Sphinx configuration (Python)
   │   ├── index.rst        # Root document with toctree
   │   ├── make.bat         # Windows build script
   │   ├── Makefile         # Unix build script
   │   ├── _build/          # Generated output (gitignore this)
   │   ├── _static/         # Static files (CSS, images)
   │   └── _templates/      # Custom templates
   ├── .venv/
   └── pyproject.toml

Step 5: Create the ubproject.toml Configuration
-----------------------------------------------

Instead of configuring sphinx-needs directly in ``conf.py``, we use a
separate ``ubproject.toml`` file. This declarative approach has
several advantages:

* **Clean separation**: Configuration is separate from Python code
* **Tooling support**: Works with ubCode (VS Code extension) for
  real-time previews, linting, and code intelligence
* **Easier maintenance**: TOML is easier to read and modify than Python
* **Schema validation**: Can be validated against a JSON schema
* **Portability**: Configuration can be consumed by other tools

.. note::

   **What is ubCode?**

   ubCode is a VS Code extension that provides a lightning-fast language
   server for Sphinx-Needs projects. It offers real-time RST previews,
   linting, smart need filtering, and editor navigation. The ``ubproject.toml``
   file is the standard configuration format for ubCode-compatible
   projects.

Create ``docs/ubproject.toml``:

.. code-block:: toml

   # Sphinx-Needs configuration in TOML format.
   # Announced to Sphinx-Needs via needs_from_toml in conf.py.
   # Schema: https://ubcode.useblocks.com/ubproject.schema.json

   "$schema" = "https://ubcode.useblocks.com/ubproject.schema.json"

   [project]
   name = "My Documentation Project"
   description = "Requirements management with Sphinx-Needs"
   srcdir = "."

   #--------------------------------------------------------------------------
   # Sphinx-Needs Configuration
   # All settings go under [needs] WITHOUT the needs_ prefix
   #--------------------------------------------------------------------------
   [needs]
   # Export needs to JSON for external tools and CI/CD integration
   build_json = true

   # Force authors to set IDs manually (recommended for stable links)
   # Without this, Sphinx-Needs auto-generates IDs from titles,
   # which break when titles change
   id_required = true

   # ID format validation using regex
   # This pattern requires: 2-10 uppercase letters/underscores,
   # optionally followed by _NNN (1-3 digits)
   # Examples: REQ_001, SPEC_42, TC_1
   id_regex = "[A-Z_]{2,10}(_[\\d]{1,3})*"

   # Additional options available for all need types
   # These become :option: fields in your RST directives
   extra_options = [
     "priority",
     "author",
     "version",
   ]

   #--------------------------------------------------------------------------
   # Need Types
   # Each [[needs.types]] entry defines a new directive you can use in RST
   #--------------------------------------------------------------------------
   [[needs.types]]
   directive = "req"           # Use as: .. req:: Title
   title = "Requirement"       # Display name in output
   prefix = "REQ_"             # Suggested ID prefix
   color = "#FFB300"           # Color in diagrams (amber)
   style = "node"              # PlantUML style: node, artifact, frame, etc.

   [[needs.types]]
   directive = "spec"
   title = "Specification"
   prefix = "SPEC_"
   color = "#ec6dd7"           # Pink/magenta
   style = "node"

   [[needs.types]]
   directive = "impl"
   title = "Implementation"
   prefix = "IMPL_"
   color = "#fa8638"           # Orange
   style = "node"

   [[needs.types]]
   directive = "test"
   title = "Test Case"
   prefix = "TC_"
   color = "#A6BDD7"           # Light blue
   style = "node"

   #--------------------------------------------------------------------------
   # Link Types
   # Define relationships between needs for traceability
   # Each link type creates bidirectional connections
   #--------------------------------------------------------------------------
   [[needs.extra_links]]
   option = "implements"         # Use as: :implements: REQ_001
   outgoing = "implements"       # Label on forward link
   incoming = "implemented by"   # Label on backward link (auto-generated)
   color = "#00AA00"             # Green in diagrams

   [[needs.extra_links]]
   option = "tests"
   outgoing = "tests"
   incoming = "tested by"
   color = "#0000AA"             # Blue

   [[needs.extra_links]]
   option = "derives"
   outgoing = "derives from"
   incoming = "derived by"
   color = "#AA0000"             # Red

.. seealso::

   For all available configuration options, see:

   * `Configuration Reference <https://sphinx-needs.readthedocs.io/en/latest/configuration.html>`_
   * `Need Types <https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-types>`_
   * `Extra Links <https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-extra-links>`_

Step 6: Configure conf.py
-------------------------

Edit ``docs/conf.py`` to enable sphinx-needs and load the TOML
configuration. The ``conf.py`` file is executed as Python, allowing
complex customization, but we keep it minimal by delegating
sphinx-needs configuration to the TOML file:

.. code-block:: python

   # docs/conf.py
   # Configuration file for the Sphinx documentation builder.
   # https://www.sphinx-doc.org/en/master/usage/configuration.html

   # -- Project information -------------------------------------------
   project = 'My Documentation Project'
   copyright = '2025, Your Name'
   author = 'Your Name'
   release = '0.1.0'

   # -- General configuration -----------------------------------------
   extensions = [
       'sphinx_needs',  # Requirements management
   ]

   templates_path = ['_templates']
   exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

   # -- Sphinx-Needs configuration ------------------------------------
   # Load configuration from external TOML file
   # This is the key line that connects sphinx-needs to ubproject.toml
   needs_from_toml = "ubproject.toml"

   # -- Options for HTML output ---------------------------------------
   html_theme = 'alabaster'
   html_static_path = ['_static']

The key line is ``needs_from_toml = "ubproject.toml"`` which tells
sphinx-needs to read its configuration from the TOML file. All
settings in the ``[needs]`` section of the TOML file are loaded
automatically.

Step 7: Create Your First Documentation
---------------------------------------

Replace the contents of ``docs/index.rst`` with:

.. code-block:: rst

   Welcome to My Documentation Project
   ====================================

   This project demonstrates requirements management with Sphinx-Needs.

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      requirements
      specifications
      traceability

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`search`

Step 8: Write Requirements
--------------------------

Create ``docs/requirements.rst``:

.. code-block:: rst

   Requirements
   ============

   This section contains all project requirements.

   System Requirements
   -------------------

   .. req:: User Authentication
      :id: REQ_001
      :status: open
      :priority: high
      :author: Your Name

      The system shall provide user authentication functionality.
      Users must be able to log in with username and password.

      **Acceptance Criteria:**

      * Users can register with email and password
      * Users can log in with valid credentials
      * Failed login attempts are logged

   .. req:: Data Persistence
      :id: REQ_002
      :status: open
      :priority: high
      :derives: REQ_001

      The system shall persist user data securely in a database.
      This requirement depends on user authentication.

   .. req:: Performance Target
      :id: REQ_003
      :status: open
      :priority: medium

      The system shall respond to API requests within 200ms
      under normal load conditions (< 1000 concurrent users).

Syntax Reference
~~~~~~~~~~~~~~~~

* ``.. req:: Title`` - Creates a requirement (the directive name comes
  from ``needs.types``)
* ``:id: REQ_001`` - Unique identifier (must match ``id_regex``)
* ``:status: open`` - Current status (custom option from ``extra_options``)
* ``:priority: high`` - Priority level (custom option)
* ``:derives: REQ_001`` - Link to another need (from ``extra_links``)

The content of a need can include any RST markup: lists, code blocks,
tables, images, and more.

Step 9: Add Specifications and Tests
------------------------------------

Create ``docs/specifications.rst``:

.. code-block:: rst

   Specifications
   ==============

   Technical specifications derived from requirements.

   Authentication Specification
   ----------------------------

   .. spec:: Login API Specification
      :id: SPEC_001
      :status: open
      :implements: REQ_001

      **Endpoint**: ``POST /api/v1/auth/login``

      **Request Body**:

      .. code-block:: json

         {
           "username": "string",
           "password": "string"
         }

      **Success Response** (200):

      .. code-block:: json

         {
           "token": "jwt-token-here",
           "expires_in": 3600
         }

      **Error Response** (401):

      .. code-block:: json

         {
           "error": "Invalid credentials"
         }

   Test Cases
   ----------

   Test cases verify that specifications are correctly implemented.

   .. test:: Login Success Test
      :id: TC_001
      :status: open
      :tests: SPEC_001

      **Preconditions**: User "testuser" exists with password "secret123"

      **Steps**:

      1. Send POST to ``/api/v1/auth/login``
      2. Include body: ``{"username": "testuser", "password": "secret123"}``

      **Expected Result**: 200 response with valid JWT token

   .. test:: Login Failure Test
      :id: TC_002
      :status: open
      :tests: SPEC_001

      **Preconditions**: User "testuser" exists

      **Steps**:

      1. Send POST to ``/api/v1/auth/login``
      2. Include body: ``{"username": "testuser", "password": "wrong"}``

      **Expected Result**: 401 response with error message

Step 10: Create Traceability Views
----------------------------------

Create ``docs/traceability.rst`` to visualize the relationships
between your needs:

.. code-block:: rst

   Traceability
   ============

   This section provides various views of requirements traceability.

   Requirements Overview
   ---------------------

   All requirements and their current status:

   .. needtable::
      :filter: type == 'req'
      :columns: id;title;status;priority
      :style: table
      :sort: id

   The ``:filter:`` option uses Python-like expressions to select needs.
   Common filters:

   * ``type == 'req'`` - All requirements
   * ``status == 'open'`` - Open items only
   * ``'auth' in title.lower()`` - Title contains "auth"

   Full Traceability Flow
   ----------------------

   This diagram shows how requirements, specifications, and tests
   connect:

   .. needflow::
      :filter: type in ['req', 'spec', 'test']
      :engine: graphviz
      :show_link_names:
      :show_legend:

   The ``needflow`` directive creates a visual flowchart of needs and
   their relationships. Use ``:show_link_names:`` to label the
   connections.

   .. note::

      We use ``:engine: graphviz`` here because Graphviz is easier to
      set up (no Java required). For more advanced diagrams and
      additional directives like ``needsequence`` or ``needuml``.

   Specifications Matrix
   ---------------------

   Which requirements are covered by specifications:

   .. needtable::
      :filter: type == 'spec'
      :columns: id;title;status;implements
      :style: table

   Test Coverage
   -------------

   Which specifications have test cases:

   .. needtable::
      :filter: type == 'test'
      :columns: id;title;status;tests
      :style: table

   Open Items
   ----------

   All items that are not yet done:

   .. needtable::
      :filter: status == 'open'
      :columns: id;type;title;status
      :style: table
      :sort: type

Step 11: Build the Documentation
--------------------------------

Generate HTML documentation:

.. code-block:: bash

   # From the project root
   uv run sphinx-build -b html docs docs/_build/html

   # Or from the docs directory using make
   cd docs
   uv run make html

Open the generated documentation:

.. code-block:: bash

   # macOS
   open docs/_build/html/index.html

   # Linux
   xdg-open docs/_build/html/index.html

   # Windows
   start docs/_build/html/index.html

You should see your documentation with:

* Styled requirement boxes with colored headers
* Clickable links between needs (both forward and backward)
* Tables showing filtered needs
* A flow diagram showing traceability

.. tip::

   For live preview during development, use ``sphinx-autobuild``:

   .. code-block:: bash

      uv add sphinx-autobuild
      uv run sphinx-autobuild docs docs/_build/html

   This automatically rebuilds when files change and refreshes your
   browser.

Final Project Structure
-----------------------

Your complete project structure:

.. code-block:: text

   my-docs-project/
   ├── docs/
   │   ├── conf.py              # Minimal Sphinx config
   │   ├── ubproject.toml       # Sphinx-Needs configuration
   │   ├── index.rst            # Main page with toctree
   │   ├── requirements.rst     # Requirements documentation
   │   ├── specifications.rst   # Specifications and test cases
   │   ├── traceability.rst     # Traceability views
   │   ├── Makefile
   │   ├── make.bat
   │   ├── _build/              # Generated output (gitignore)
   │   │   └── html/
   │   │       └── needs.json   # Exported needs data
   │   ├── _static/
   │   └── _templates/
   ├── .venv/                   # Virtual environment (gitignore)
   ├── .python-version
   └── pyproject.toml

Understanding ubproject.toml
----------------------------

The ``ubproject.toml`` file follows a specific structure. Here's a
reference of the key sections:

Project Metadata
~~~~~~~~~~~~~~~~

.. code-block:: toml

   [project]
   name = "Project Name"
   description = "Project description"
   srcdir = "."               # Source directory relative to toml file

Basic Needs Settings
~~~~~~~~~~~~~~~~~~~~

All settings go under ``[needs]`` **without** the ``needs_`` prefix:

.. code-block:: toml

   [needs]
   build_json = true          # Export needs to JSON
   id_required = true         # Require manual IDs (recommended)
   id_regex = "..."           # ID format validation
   title_optional = false     # Require titles on needs

Extra Options
~~~~~~~~~~~~~

Add custom fields available on all need types:

.. code-block:: toml

   extra_options = [
     "priority",              # :priority: high
     "author",                # :author: John Doe
     "version",               # :version: 1.0
   ]

Need Types
~~~~~~~~~~

Use ``[[needs.types]]`` (double brackets for arrays):

.. code-block:: toml

   [[needs.types]]
   directive = "req"          # RST directive: .. req::
   title = "Requirement"      # Display title
   prefix = "REQ_"            # ID prefix
   color = "#FFB300"          # Hex color for diagrams
   style = "node"             # PlantUML style

Available styles: ``node``, ``artifact``, ``frame``, ``storage``, ``database``,
``actor``

Link Types
~~~~~~~~~~

Use ``[[needs.extra_links]]`` for traceability relationships:

.. code-block:: toml

   [[needs.extra_links]]
   option = "implements"      # RST option: :implements:
   outgoing = "implements"    # Forward link label
   incoming = "implemented by"  # Auto-generated backward link
   color = "#00AA00"          # Link color in diagrams

.. note::

   As of sphinx-needs 6.1.0, the ``incoming`` and ``outgoing`` fields are
   optional. If omitted, the option name is used as the default label.

Schema Validation (sphinx-needs 6.0+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with sphinx-needs 6.0, you can define typed extra options
with JSON schema constraints. This provides validation for custom
fields:

.. code-block:: toml

   # Typed extra options with validation
   [[needs.extra_options]]
   name = "priority"
   schema.type = "string"
   schema.enum = ["low", "medium", "high", "critical"]

   [[needs.extra_options]]
   name = "effort_hours"
   schema.type = "integer"
   schema.minimum = 1
   schema.maximum = 1000

   [[needs.extra_options]]
   name = "verified"
   schema.type = "boolean"

This approach provides:

* **Type checking** - Ensure values match expected types (string,
  integer, boolean, array)
* **Enum constraints** - Restrict values to a predefined set
* **Range validation** - Set minimum/maximum for numeric fields
* **Build-time warnings** - Invalid values trigger warnings during build

When schema violations occur, sphinx-needs generates a ``schema_violations.json``
file alongside ``needs.json`` for debugging.

VS Code Setup with ubCode
-------------------------

For the best editing experience, install the ubCode extension:

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "ubCode"
4. Install the extension

ubCode provides:

* **Real-time RST preview** - See your documentation as you type
* **Linting** - Catch errors before building
* **Code intelligence** - Auto-complete for need IDs and links
* **Navigation** - Jump to need definitions

Additional recommended extensions:

* **Even Better TOML** - TOML syntax highlighting and validation
* **Python** - Python language support for conf.py

Create ``.vscode/settings.json``:

.. code-block:: json

   {
     "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
   }

Common Commands Reference
-------------------------

.. code-block:: bash

   # Build HTML documentation
   uv run sphinx-build -b html docs docs/_build/html

   # Build with live reload (requires sphinx-autobuild)
   uv run sphinx-autobuild docs docs/_build/html

   # Clean build directory
   rm -rf docs/_build

   # Build with warnings as errors (useful for CI)
   uv run sphinx-build -W -b html docs docs/_build/html

   # Check for broken links
   uv run sphinx-build -b linkcheck docs docs/_build/linkcheck

   # Generate PDF (requires LaTeX)
   uv run sphinx-build -b latex docs docs/_build/latex
   cd docs/_build/latex && make

Next Steps
----------

Now that you have a working Sphinx-Needs project, explore these
topics:

**Enhance Your Configuration:**

* Add more need types for your domain (user stories, bugs, features)
* Define constraints to validate needs (e.g., require status on all
  requirements)
* Create custom layouts to change how needs are displayed

**Visualization:**

* Use ``needpie`` and ``needbar`` for metrics charts
* Use ``needgantt`` for timeline views
* Customize ``needflow`` with different engines (graphviz vs plantuml)

**Integration:**

* Import needs from external JSON files with ``needimport``
* Use the generated ``needs.json`` in CI/CD pipelines
* Connect to Jira or other tools via external needs

**Themes:**

Try a better theme for your documentation:

.. code-block:: bash

   uv add furo

Then in ``conf.py``:

.. code-block:: python

   html_theme = 'furo'

Version History and Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're upgrading from an older version of sphinx-needs, be aware of
these important changes:

**sphinx-needs 6.3.0:**

* File paths specified in ``needs_from_toml`` now resolve relative to
  the TOML file location, not relative to ``conf.py``

**sphinx-needs 6.1.0:**

* The ``incoming`` and ``outgoing`` fields in ``extra_links`` are now
  optional

**sphinx-needs 6.0.0:**

* Requires Sphinx 7.4+ and Python 3.10+
* Introduced JSON schema validation for extra options
* Removed deprecated ``needfilter`` directive (use ``needtable`` or ``needlist``
  instead)
* Variant syntax changed to require ``<< >>`` wrappers
* Default values only apply to missing/None fields (not falsy values
  like empty strings)

Official Documentation
~~~~~~~~~~~~~~~~~~~~~~

* `Sphinx Documentation <https://www.sphinx-doc.org/>`_
* `Sphinx-Needs Documentation <https://sphinx-needs.readthedocs.io/>`_
* `Sphinx-Needs Configuration <https://sphinx-needs.readthedocs.io/en/latest/configuration.html>`_
* `ubCode Documentation <https://ubcode.useblocks.com/>`_
* `uv Documentation <https://docs.astral.sh/uv/>`_

Troubleshooting
---------------

**Build fails with "Unknown directive type 'req'"**

Ensure ``sphinx_needs`` is in the ``extensions`` list in ``conf.py``
and that ``needs_from_toml`` points to the correct file.

.. code-block:: python

   extensions = ['sphinx_needs']
   needs_from_toml = "ubproject.toml"

**"Module sphinx_needs not found"**

Run ``uv add sphinx-needs==6.3.0`` and ensure you're using ``uv run``
or have activated the virtual environment.

**TOML configuration not loading**

Verify that:

1. ``needs_from_toml = "ubproject.toml"`` is set in ``conf.py``
2. The file ``docs/ubproject.toml`` exists
3. The TOML syntax is valid (check with a TOML validator)

**Needflow diagrams not rendering**

The ``needflow`` directive supports two rendering engines:

1. **Graphviz** (recommended for getting started) - Requires only the
   Graphviz system package. Use ``:engine: graphviz`` in your directive.
2. **PlantUML** (default) - Requires Java + PlantUML JAR +
   sphinxcontrib-plantuml. Provides more styling options.

Install Graphviz for basic diagram generation:

.. code-block:: bash

   # macOS
   brew install graphviz

   # Ubuntu/Debian
   sudo apt install graphviz

   # Windows (via chocolatey)
   choco install graphviz

**PlantUML errors (Java/JAR not found)**

If you see errors like ``plantuml command cannot be run`` or ``FileNotFoundError: java``,
you're using the default PlantUML engine without proper setup. You
have two options:

1. **Quick fix**: Add ``:engine: graphviz`` to your ``needflow``
   directives
2. **Full setup**: Follow :ref:`tutorial-plantuml-setup` to install
   PlantUML

To set Graphviz as the default engine for all needflow directives, add
to ``conf.py``:

.. code-block:: python

   needs_flow_engine = "graphviz"

**ID validation errors**

Check that your IDs match the pattern in ``id_regex``. The default
pattern ``[A-Z_]{2,10}(_[\d]{1,3})*`` requires:

* 2-10 uppercase letters or underscores
* Optionally followed by ``_`` and 1-3 digits
* Valid: ``REQ_001``, ``SPEC_42``, ``TC_1``, ``USER_STORY``
* Invalid: ``req_001`` (lowercase), ``R_1234`` (4 digits), ``A`` (too
  short)

**Changes not appearing after rebuild**

Sphinx caches build artifacts. Delete the build directory and rebuild:

.. code-block:: bash

   rm -rf docs/_build
   uv run sphinx-build -b html docs docs/_build/html

**Links between needs not working**

Ensure the target need ID exists and is spelled correctly. IDs are
case-sensitive. Use the generated ``needs.json`` to verify all IDs.

**Schema validation warnings (sphinx-needs 6.0+)**

If you're using typed extra options with schema validation, you may
see warnings like ``sn_schema_warning`` or ``sn_schema_violation``. To
suppress specific warning types, add to ``conf.py``:

.. code-block:: python

   suppress_warnings = [
       "sn_schema_info",      # Informational messages
       "sn_schema_warning",   # Non-critical warnings
       # "sn_schema_violation",  # Keep violations visible
   ]

Check the ``schema_violations.json`` file in your build output for
details about validation failures.

Next Steps
----------

Now that you have a working sphinx-needs project, explore these
topics:

* :ref:`tutorial-plantuml-setup` - Enable PlantUML for advanced diagrams
  (needsequence, needuml, needgantt)
* :ref:`tutorial-creating-dashboards` - Create visual dashboards with
  charts and diagrams
* :ref:`how-to-write-requirements` - Best practices for writing
  requirements
* :ref:`external-needs` - Import needs from external systems like Jira

.. seealso::

   **sphinx-needs Reference:**

   * `Official sphinx-needs Docs <https://sphinx-needs.readthedocs.io/en/latest/>`_
     - Getting started guide
   * `Directives Reference <https://sphinx-needs.readthedocs.io/en/latest/directives/index.html>`_
     - All available directives
   * `Configuration Options <https://sphinx-needs.readthedocs.io/en/latest/configuration.html>`_
     - Complete configuration reference
   * `Filter Expressions <https://sphinx-needs.readthedocs.io/en/latest/filter.html>`_
     - Query and filter your needs
   * `Layouts & Styles <https://sphinx-needs.readthedocs.io/en/latest/layout_styles.html>`_
     - Customize how needs are displayed

   **Related Tools:**

   * `Official Sphinx Docs <https://www.sphinx-doc.org/en/master/>`_ -
     Sphinx documentation generator
   * `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
     - RST syntax guide
