.. _reference:

:octicon:`book` Reference
======================================

A curated collection of tools, libraries, and resources for **X-as-Code**
and **Sphinx-Needs** based documentation workflows.

Inspired by other "awesome-XXX" collections.

----

useblocks Open Source
---------------------

The core ecosystem of open-source tools from `useblocks <https://useblocks.com>`_ for
x-as-code workflows.

Requirements & Traceability
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Sphinx-Needs <https://github.com/useblocks/sphinx-needs>`_ - The flagship extension for requirements management in Sphinx. Define, link, and trace needs, requirements, specs, and test cases. Supports compliance standards like DO-178B/C and ISO 26262. 341K+ downloads.
* `Sphinx-Test-Reports <https://github.com/useblocks/sphinx-test-reports>`_ - Import test results from JUnit XML files as need objects. Link test results to specifications for full traceability.
* `Sphinx-Modeling <https://github.com/useblocks/sphinx-modeling>`_ - Pydantic-based models and constraints for Sphinx-Needs objects. Define schemas and validate need structures.
* `Sphinx-Codelinks <https://github.com/useblocks/sphinx-codelinks>`_ - Create Sphinx-Needs items directly from source code comments. Bridge the gap between code and documentation.

Build & Output
~~~~~~~~~~~~~~

* `Sphinx-SimplePDF <https://github.com/useblocks/sphinx-simplepdf>`_ - A simple PDF builder for Sphinx using WeasyPrint and SCSS styling. Create professional PDFs without LaTeX.
* `Bazel-Drives-Sphinx <https://github.com/useblocks/bazel-drives-sphinx>`_ - Use Bazel as the build system for Sphinx documentation projects.

Content Management
~~~~~~~~~~~~~~~~~~

* `Sphinx-Collections <https://github.com/useblocks/sphinx-collections>`_ - Collect and manage files from multiple sources (Git repos, symlinks, Jinja templates) into your Sphinx project.
* `Sphinx-Data-Viewer <https://github.com/useblocks/sphinx-data-viewer>`_ - Display JSON and Python data structures in readable list format within documentation.
* `Sphinx-Preview <https://github.com/useblocks/sphinx-preview>`_ - Add hover-activated link previews for enhanced navigation.

Integrations
~~~~~~~~~~~~

* `Sphinx-EMF <https://github.com/useblocks/sphinx-emf>`_ - Connect Sphinx-Needs to Eclipse Modeling Framework (EMF) models. Import and synchronize EMF-based data.
* `libpdf <https://github.com/useblocks/libpdf>`_ - Extract structured data from PDF documents. Useful for importing legacy requirements.

----

useblocks Commercial
--------------------

Enterprise-grade tools for professional engineering teams requiring ALM integration
and advanced traceability.

* `ubConnect <https://useblocks.com>`_ - Standalone connector that syncs ALM data with Sphinx-Needs. Supports DOORS, Polarion, Codebeamer, Jama, Jira, plus Excel, ReqIF, and SysML v2.
* `ubCode <https://useblocks.com>`_ - VS Code extension for creating structured, reusable building blocks with instant preview, validation, and traceability links.
* `ubTrace <https://useblocks.com>`_ - Real-time traceability dashboard across development artifacts. Shows relationships, versions, and change logs for audits and analysis.

----

Sphinx Extensions
-----------------

Essential Sphinx extensions for documentation-as-code workflows.

Content & Authoring
~~~~~~~~~~~~~~~~~~~

* `MyST-Parser <https://myst-parser.readthedocs.io/>`_ - Write Sphinx documentation in Markdown with MyST syntax. Full RST feature parity.
* `sphinx-design <https://sphinx-design.readthedocs.io/>`_ - Responsive web design components: grids, cards, tabs, dropdowns, badges.
* `sphinx-tabs <https://sphinx-tabs.readthedocs.io/>`_ - Create tabbed content areas for code examples and multi-platform instructions.
* `sphinx-copybutton <https://sphinx-copybutton.readthedocs.io/>`_ - Add copy buttons to code blocks for easy code sharing.
* `sphinx-togglebutton <https://sphinx-togglebutton.readthedocs.io/>`_ - Toggle visibility of content sections.

API Documentation
~~~~~~~~~~~~~~~~~

* `sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ - Generate documentation from Python docstrings automatically.
* `sphinx.ext.napoleon <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_ - Support for NumPy and Google style docstrings.
* `sphinx-autodoc-typehints <https://github.com/tox-dev/sphinx-autodoc-typehints>`_ - Type hints support in autodoc output.
* `Breathe <https://breathe.readthedocs.io/>`_ - Bridge between Sphinx and Doxygen for C/C++ documentation.

Diagrams & Visualization
~~~~~~~~~~~~~~~~~~~~~~~~

* `sphinxcontrib-mermaid <https://sphinxcontrib-mermaid-demo.readthedocs.io/>`_ - Embed Mermaid diagrams (flowcharts, sequence diagrams, Gantt charts).
* `sphinxcontrib-plantuml <https://github.com/sphinx-contrib/plantuml>`_ - Embed PlantUML diagrams for UML modeling.
* `sphinx-gallery <https://sphinx-gallery.github.io/>`_ - Build galleries from Python scripts with auto-generated output.

Notebooks & Interactive
~~~~~~~~~~~~~~~~~~~~~~~

* `nbsphinx <https://nbsphinx.readthedocs.io/>`_ - Jupyter notebook integration for Sphinx.
* `Jupyter Book <https://jupyterbook.org/>`_ - Build publication-quality books from Jupyter notebooks and Markdown.
* `sphinx-autobuild <https://github.com/executablebooks/sphinx-autobuild>`_ - Live preview with auto-rebuild on file changes.

Cross-Referencing
~~~~~~~~~~~~~~~~~

* `sphinx.ext.intersphinx <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_ - Link to other Sphinx documentation projects.
* `sphinx.ext.viewcode <https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html>`_ - Add links to highlighted source code.
* `sphinxcontrib-bibtex <https://sphinxcontrib-bibtex.readthedocs.io/>`_ - BibTeX citations for academic documentation.

----

Sphinx Themes
-------------

Popular themes for professional documentation appearance.

* `Furo <https://pradyunsg.me/furo/>`_ - Clean, customizable theme with excellent mobile support and dark mode.
* `sphinx-rtd-theme <https://sphinx-rtd-theme.readthedocs.io/>`_ - The Read the Docs theme. Industry standard for open source projects.
* `PyData Sphinx Theme <https://pydata-sphinx-theme.readthedocs.io/>`_ - Theme for scientific and data-focused projects. Used by NumPy, Pandas.
* `sphinx-book-theme <https://sphinx-book-theme.readthedocs.io/>`_ - Theme designed for Jupyter Book with clean layout.
* `Alabaster <https://alabaster.readthedocs.io/>`_ - Minimalist theme, Sphinx default. Clean and lightweight.
* `sphinx-immaterial <https://sphinx-immaterial.readthedocs.io/>`_ - Material Design theme based on mkdocs-material.

----

Hosting & CI/CD
---------------

Platforms and tools for hosting and automating documentation builds.

* `Read the Docs <https://readthedocs.org/>`_ - Free documentation hosting with automatic builds from Git. Supports versioning.
* `GitHub Pages <https://pages.github.com/>`_ - Free static hosting from GitHub repositories.
* `GitHub Actions <https://github.com/features/actions>`_ - Automate Sphinx builds in CI/CD pipelines.
* `GitLab Pages <https://docs.gitlab.com/ee/user/project/pages/>`_ - Static site hosting integrated with GitLab CI/CD.
* `Netlify <https://www.netlify.com/>`_ - Modern hosting platform with preview deployments.

----

Data Formats & Standards
------------------------

Standards and formats relevant to engineering documentation and requirements exchange.

* `ReqIF <https://www.omg.org/spec/ReqIF/>`_ - Requirements Interchange Format. OMG standard for exchanging requirements between tools.
* `SysML v2 <https://www.omgsysml.org/>`_ - Systems Modeling Language for model-based systems engineering.
* `SPDX <https://spdx.dev/>`_ - Software Package Data Exchange for license compliance.
* `OpenAPI/Swagger <https://swagger.io/specification/>`_ - API specification standard with Sphinx integration via sphinxcontrib-openapi.

----

Learning Resources
------------------

Tutorials, documentation, and examples for getting started.

* `Sphinx Documentation <https://www.sphinx-doc.org/>`_ - Official Sphinx documentation and tutorials.
* `Sphinx-Needs Documentation <https://sphinx-needs.readthedocs.io/>`_ - Complete guide to Sphinx-Needs directives, configuration, and features.
* `Sphinx-Needs Demo <https://github.com/useblocks/sphinx-needs-demo>`_ - Example project showcasing automotive software documentation patterns.
* `Write the Docs <https://www.writethedocs.org/>`_ - Community and resources for documentation practitioners.
* `Docs as Code <https://www.docslikecode.com/>`_ - Resources for treating documentation like source code.

----

Contributing
------------

Know a tool that should be on this list? Open an issue or pull request!

