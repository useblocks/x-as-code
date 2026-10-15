.. _drawio-integration:

:octicon:`workflow` Draw.io Integration
=======================================

Draw.io (diagrams.net) is a powerful, free diagramming tool that can be used to create various types of diagrams including flowcharts, network diagrams, UML diagrams, and more. This guide shows how to integrate Draw.io diagrams into your Sphinx documentation.

Workflow Overview
-----------------

The integration process involves three main steps:

1. Create and edit your diagram in Draw.io
2. Export the diagram as HTML
3. Embed the HTML in your RST document

Step 1: Create Your Diagram
----------------------------

1. Open `Draw.io <https://app.diagrams.net/>`_ in your browser or use the desktop application
2. Create your diagram using the Draw.io editor
3. Save the file with a ``.drawio`` extension (this is your source file for editing)

.. tip::

   Keep your ``.drawio`` source files in your documentation directory so you can easily update them later.

Step 2: Export as HTML
-----------------------

Once you're satisfied with your diagram:

1. In Draw.io, go to **File** → **Export as** → **HTML**
2. Save the HTML file with a descriptive name (e.g., ``my-diagram.drawio.html``)
3. Place the HTML file in the same directory as your RST document (or in a subdirectory)

.. note::

   The exported HTML file is self-contained and includes all the diagram data inline.

Step 3: Embed in RST Document
------------------------------

Use the ``raw`` directive to embed the Draw.io HTML in your RST document:

.. code-block:: restructuredtext

   .. raw:: html
      :file: ./my-diagram.drawio.html

Example Diagram
---------------

Here's a workflow diagram showing the Draw.io integration process itself:

.. raw:: html
   :file: ./_diagrams/example-workflow.drawio.html

This diagram illustrates:

* The linear workflow from creation to documentation build
* A feedback loop for updating diagrams (shown with dashed lines)
* Color-coding: green for start, blue for process steps, yellow for decision, red for end

Working with Multiple Tabs
---------------------------

Draw.io supports multiple tabs (pages) in a single diagram file. When viewing the HTML export in a browser, you can navigate between tabs.

.. caution::

   **For PDF Export**: If you plan to export your documentation as PDF, create separate Draw.io files for each tab/page. PDF export typically only shows one tab, so having multiple tabs may cause content to be hidden.

Best Practices
--------------

1. **Source Control**: Keep both the ``.drawio`` source files and the ``.drawio.html`` exports in your repository
2. **File Naming**: Use descriptive names like ``authentication-flow.drawio.html``
3. **Directory Structure**: Consider organizing diagrams in a subdirectory like ``_diagrams/``
4. **Update Process**: When updating diagrams, edit the ``.drawio`` file and re-export to HTML
5. **Accessibility**: Add descriptive text around diagrams to explain what they represent

Example Directory Structure
----------------------------

.. code-block:: text

   docs/
   ├── how-to-guides/
   │   └── my-guide/
   │       ├── index.rst
   │       └── _diagrams/
   │           ├── workflow.drawio           # Source file
   │           ├── workflow.drawio.html      # Exported HTML
   │           ├── architecture.drawio
   │           └── architecture.drawio.html

Using with Sphinx-Needs
------------------------

You can also embed Draw.io diagrams inside Sphinx-Needs to enable traceability:

.. code-block:: restructuredtext

   .. arch:: System Architecture with Draw.io
      :id: ARCH_005

      This architecture diagram shows the system components:

      .. raw:: html
         :file: ./_diagrams/system-architecture.drawio.html

Alternative: Inline HTML
------------------------

Instead of using ``:file:``, you can also embed the HTML content directly:

.. code-block:: restructuredtext

   .. raw:: html

      <div class="mxgraph" style="max-width:100%;">
      <!-- Draw.io HTML content here -->
      </div>

This approach is useful when you want to share a single RST file without external dependencies.

Additional Resources
--------------------

* `Draw.io Official Website <https://www.diagrams.net/>`_
* `Draw.io Documentation <https://www.diagrams.net/doc/>`_
* `Raw Data Pass-Through directive <https://docutils.sourceforge.io/docs/ref/rst/directives.html#raw-data-pass-through>`_
