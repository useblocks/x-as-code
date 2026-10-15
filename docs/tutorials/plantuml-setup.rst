.. _tutorial-plantuml-setup:

:octicon:`file-code` Setting Up PlantUML for Sphinx-Needs
=========================================================

This tutorial guides you through setting up PlantUML to unlock
advanced diagram capabilities in sphinx-needs. By the end, you'll be
able to generate sequence diagrams, custom UML diagrams, Gantt charts,
and richly styled flow diagrams.

.. note::

   **Target audience**: Developers who have completed
   :ref:`tutorial-sphinx-needs-setup` and want to enable advanced
   visualization features.

Why PlantUML?
-------------

Sphinx-needs supports two rendering engines for diagrams:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Engine
     - Advantages
     - Limitations
   * - **Graphviz**
     - No Java required, fast, simple setup
     - Basic styling only, limited diagram types
   * - **PlantUML**
     - Rich styling, many diagram types, themes
     - Requires Java + JAR file setup

**PlantUML is required for these sphinx-needs directives:**

* ``needsequence`` - Sequence diagrams showing interactions between needs
* ``needuml`` - Custom PlantUML diagrams with Jinja templating
* ``needarch`` - Architecture diagrams embedded in needs
* ``needgantt`` - Gantt charts for timeline views

**PlantUML is optional (but recommended) for:**

* ``needflow`` - Can use either Graphviz or PlantUML engine

Prerequisites
-------------

Before starting, ensure you have:

* A working sphinx-needs project (see :ref:`tutorial-sphinx-needs-setup`)
* Terminal/command line access
* Administrator access to install system packages

Step 1: Install Java
--------------------

PlantUML requires Java Runtime Environment (JRE) version 8 or higher.

**Check if Java is installed:**

.. code-block:: bash

   java -version

If installed, you'll see output like:

.. code-block:: text

   openjdk version "17.0.2" 2022-01-18
   OpenJDK Runtime Environment (build 17.0.2+8-86)

**Install Java if needed:**

.. tab-set::

   .. tab-item:: macOS

      .. code-block:: bash

         # Using Homebrew
         brew install openjdk

         # Add to PATH (for Apple Silicon Macs)
         echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc
         source ~/.zshrc

   .. tab-item:: Ubuntu/Debian

      .. code-block:: bash

         sudo apt update
         sudo apt install default-jre

   .. tab-item:: Windows

      .. code-block:: bash

         # Using Chocolatey
         choco install openjdk

         # Or download from: https://adoptium.net/

Step 2: Install Graphviz (Recommended)
--------------------------------------

While PlantUML can generate many diagrams without Graphviz, some
diagram types (class diagrams, object diagrams, component diagrams)
require Graphviz for layout.

.. tab-set::

   .. tab-item:: macOS

      .. code-block:: bash

         brew install graphviz

   .. tab-item:: Ubuntu/Debian

      .. code-block:: bash

         sudo apt install graphviz

   .. tab-item:: Windows

      .. code-block:: bash

         choco install graphviz

**Verify installation:**

.. code-block:: bash

   dot -version

Step 3: Download PlantUML JAR
-----------------------------

Download the PlantUML JAR file and place it in your project:

.. code-block:: bash

   # Create a utils directory in your docs folder
   mkdir -p docs/utils

   # Download PlantUML JAR
   curl -L -o docs/utils/plantuml.jar \
       https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar

.. tip::

   Check for the latest version at
   `PlantUML releases <https://github.com/plantuml/plantuml/releases>`_.

**Verify PlantUML installation:**

.. code-block:: bash

   java -jar docs/utils/plantuml.jar -testdot

You should see output indicating that Graphviz is properly configured:

.. code-block:: text

   Dot version: dot - graphviz version 2.43.0 (0)
   Installation seems OK. File generation OK

Step 4: Install sphinxcontrib-plantuml
--------------------------------------

Add the sphinxcontrib-plantuml extension to your project:

.. code-block:: bash

   uv add sphinxcontrib-plantuml

This extension handles the communication between Sphinx and PlantUML.

Step 5: Configure conf.py
-------------------------

Update your ``conf.py`` to enable PlantUML:

.. code-block:: python

   import os

   # -- General configuration -----------------------------------------
   extensions = [
       'sphinxcontrib.plantuml',  # PlantUML support
       'sphinx.ext.graphviz',     # Graphviz fallback (optional)
       'sphinx_needs',            # Requirements management
   ]

   # -- PlantUML configuration ----------------------------------------
   # Path to PlantUML JAR (relative to conf.py location)
   plantuml = f'java -jar {os.path.join(os.path.dirname(__file__), "utils", "plantuml.jar")}'

   # Output format: 'svg' recommended for quality and scalability
   plantuml_output_format = 'svg'

   # Show syntax errors as images (helpful for debugging)
   plantuml_syntax_error_image = True

   # -- Sphinx-Needs configuration ------------------------------------
   needs_from_toml = "ubproject.toml"

   # Optional: Set PlantUML as default engine for needflow
   # needs_flow_engine = "plantuml"

.. note::

   **Headless Mode for CI/CD:**

   If running in environments without a display (Docker, CI servers),
   add the headless flag:

   .. code-block:: python

      plantuml = f'java -Djava.awt.headless=true -jar {os.path.join(os.path.dirname(__file__), "utils", "plantuml.jar")}'

Step 6: Using PlantUML Diagrams
-------------------------------

Now you can use all PlantUML-powered sphinx-needs directives.

needflow with PlantUML
~~~~~~~~~~~~~~~~~~~~~~

The ``needflow`` directive can use PlantUML for richer styling:

.. code-block:: rst

   .. needflow:: Requirements Traceability
      :filter: type in ['req', 'spec', 'test']
      :engine: plantuml
      :show_link_names:
      :show_legend:

With PlantUML, you can apply custom styles using the ``:config:``
option:

.. code-block:: rst

   .. needflow:: Styled Flow Diagram
      :filter: type == 'req'
      :engine: plantuml
      :config: monochrome

needsequence
~~~~~~~~~~~~

Create sequence diagrams showing interactions between needs:

.. code-block:: rst

   .. needsequence:: Login Sequence
      :start: SPEC_001

This generates a UML sequence diagram starting from the specified need
and following its links.

needuml
~~~~~~~

Create custom PlantUML diagrams with Jinja templating:

.. code-block:: rst

   .. needuml::

      @startuml
      !theme plain

      package "Requirements" {
        {% for need in filter("type == 'req'") %}
        [{{ need.title }}] as {{ need.id }}
        {% endfor %}
      }

      package "Specifications" {
        {% for need in filter("type == 'spec'") %}
        [{{ need.title }}] as {{ need.id }}
        {% endfor %}
      }

      {% for need in filter("type == 'spec'") %}
      {% for impl in need.implements %}
      {{ impl }} --> {{ need.id }}
      {% endfor %}
      {% endfor %}

      @enduml

The Jinja templating allows you to dynamically generate diagrams based
on your actual needs data.

needgantt
~~~~~~~~~

Create Gantt charts for timeline visualization:

.. code-block:: rst

   .. needgantt:: Project Timeline
      :filter: type == 'req'
      :duration_option: effort_days
      :completion_option: progress

.. note::

   ``needgantt`` requires the ``duration_option`` to specify which
   need option contains the duration in days.

Step 7: PlantUML Styling
------------------------

Define custom PlantUML styles in ``conf.py``:

.. code-block:: python

   # Custom PlantUML configurations
   needs_flow_configs = {
       "monochrome": """
           skinparam monochrome true
           skinparam shadowing false
       """,
       "handwritten": """
           skinparam handwritten true
           skinparam monochrome true
       """,
       "colorful": """
           skinparam shadowing false
           skinparam roundcorner 10
           skinparam componentStyle uml2
           skinparam defaultFontSize 12
       """,
       "lefttoright": """
           left to right direction
       """,
   }

Apply styles in your directives:

.. code-block:: rst

   .. needflow:: Handwritten Style
      :filter: type == 'req'
      :engine: plantuml
      :config: handwritten, lefttoright

Multiple configurations are applied in order, allowing you to combine
them.

Need Type Styles
~~~~~~~~~~~~~~~~

The ``style`` field in your need types (defined in ``ubproject.toml``)
controls how needs appear in PlantUML diagrams:

.. code-block:: toml

   [[needs.types]]
   directive = "req"
   title = "Requirement"
   prefix = "REQ_"
   color = "#FFB300"
   style = "node"          # or: artifact, frame, storage, database, actor

Available PlantUML styles:

* ``node`` - Default rectangular box
* ``artifact`` - Document-like shape
* ``frame`` - Frame/container shape
* ``storage`` - Cylinder shape (good for data)
* ``database`` - Database cylinder
* ``actor`` - Stick figure (good for user stories)

Step 8: Debugging PlantUML
--------------------------

Use the ``:debug:`` option to see generated PlantUML code:

.. code-block:: rst

   .. needflow:: Debug Example
      :filter: type == 'req'
      :engine: plantuml
      :debug:

This outputs the raw PlantUML code after the rendered image, helping
you troubleshoot issues.

Save generated code for external testing:

.. code-block:: rst

   .. needuml::
      :save: debug_output.puml

      @startuml
      Alice -> Bob: Hello
      @enduml

Step 9: CI/CD Configuration
---------------------------

GitHub Actions Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # .github/workflows/docs.yml
   name: Build Documentation

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.12'

         - name: Install system dependencies
           run: |
             sudo apt-get update
             sudo apt-get install -y default-jre graphviz

         - name: Download PlantUML
           run: |
             mkdir -p docs/utils
             curl -L -o docs/utils/plantuml.jar \
               https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar

         - name: Install Python dependencies
           run: |
             pip install uv
             uv sync

         - name: Build documentation
           run: |
             uv run sphinx-build -W -b html docs docs/_build/html

         - name: Upload artifact
           uses: actions/upload-artifact@v4
           with:
             name: documentation
             path: docs/_build/html

ReadTheDocs Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

ReadTheDocs provides PlantUML pre-installed. Create ``.readthedocs.yaml``:

.. code-block:: yaml

   version: 2

   build:
     os: ubuntu-22.04
     tools:
       python: "3.12"
     apt_packages:
       - default-jre
       - graphviz

   python:
     install:
       - method: pip
         path: .

Update ``conf.py`` for ReadTheDocs compatibility:

.. code-block:: python

   import os

   # Detect ReadTheDocs environment
   on_rtd = os.environ.get('READTHEDOCS') == 'True'

   if on_rtd:
       # ReadTheDocs provides plantuml.jar
       plantuml = 'java -Djava.awt.headless=true -jar /usr/share/plantuml/plantuml.jar'
   else:
       # Local development
       plantuml = f'java -jar {os.path.join(os.path.dirname(__file__), "utils", "plantuml.jar")}'

Docker Configuration
~~~~~~~~~~~~~~~~~~~~

Create a ``Dockerfile`` for consistent builds:

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       default-jre \
       graphviz \
       curl \
       && rm -rf /var/lib/apt/lists/*

   # Download PlantUML
   RUN curl -L -o /opt/plantuml.jar \
       https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar

   ENV PLANTUML_JAR=/opt/plantuml.jar

   WORKDIR /docs

   # Install Python dependencies
   COPY pyproject.toml .
   RUN pip install uv && uv sync

   CMD ["uv", "run", "sphinx-build", "-b", "html", ".", "_build/html"]

Troubleshooting
---------------

**"plantuml command cannot be run"**

The JAR file path is incorrect. Verify:

1. The JAR file exists at the specified path
2. The path in ``conf.py`` is correct (use ``os.path.dirname(__file__)``
   for relative paths)

.. code-block:: bash

   # Test PlantUML directly
   java -jar docs/utils/plantuml.jar -version

**"FileNotFoundError: java"**

Java is not installed or not in PATH:

.. code-block:: bash

   # Check Java installation
   java -version

   # On macOS, you may need to add to PATH
   export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

**Syntax errors in generated diagrams**

Use the ``:debug:`` option to see the generated PlantUML code:

.. code-block:: rst

   .. needflow::
      :filter: type == 'req'
      :debug:

Then test the code with PlantUML directly:

.. code-block:: bash

   java -jar docs/utils/plantuml.jar -tpng diagram.puml

**Diagrams not rendering in CI/CD**

Ensure headless mode is enabled:

.. code-block:: python

   plantuml = 'java -Djava.awt.headless=true -jar /path/to/plantuml.jar'

**Graphviz errors in PlantUML**

Some diagram types require Graphviz. Install it and verify:

.. code-block:: bash

   java -jar docs/utils/plantuml.jar -testdot

**Build is slow with many diagrams**

PlantUML JVM startup adds overhead. Consider:

1. Using Graphviz for simple ``needflow`` diagrams
2. Enabling PlantUML server mode (advanced)
3. Caching build artifacts

Project Structure
-----------------

After completing this tutorial, your project structure should include:

.. code-block:: text

   my-docs-project/
   ├── docs/
   │   ├── conf.py              # PlantUML configuration
   │   ├── ubproject.toml       # Sphinx-Needs configuration
   │   ├── utils/
   │   │   └── plantuml.jar     # PlantUML JAR file
   │   ├── index.rst
   │   └── ...
   ├── .github/
   │   └── workflows/
   │       └── docs.yml         # CI/CD workflow
   └── pyproject.toml

Next Steps
----------

Now that PlantUML is configured, explore these advanced features:

* ``needpie`` and ``needbar`` - Create charts for metrics visualization
* Custom PlantUML themes - Apply corporate styling to diagrams
* PlantUML includes - Reuse diagram components across your documentation

.. seealso::

   **PlantUML Reference:**

   * `PlantUML Documentation <https://plantuml.com/>`_ - Complete PlantUML guide
   * `PlantUML Themes <https://plantuml.com/theme>`_ - Available themes
   * `PlantUML Language Reference <https://plantuml.com/guide>`_ - Syntax reference

   **sphinx-needs Diagram Directives:**

   * `needflow <https://sphinx-needs.readthedocs.io/en/latest/directives/needflow.html>`_ - Flow diagrams
   * `needsequence <https://sphinx-needs.readthedocs.io/en/latest/directives/needsequence.html>`_ - Sequence diagrams
   * `needuml <https://sphinx-needs.readthedocs.io/en/latest/directives/needuml.html>`_ - Custom PlantUML
   * `needgantt <https://sphinx-needs.readthedocs.io/en/latest/directives/needgantt.html>`_ - Gantt charts
