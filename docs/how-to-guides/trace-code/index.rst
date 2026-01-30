.. _src-tracing:

:octicon:`link` Tracing Source Code
===================================

This guide explains how to use CodeLinks to trace source code files
and lines to needs in your documentation.

**Step 1: Install CodeLinks**

Follow the installation instructions in the `CodeLinks documentation <https://codelinks.useblocks.com/basics/installation.html>`__.

**Step 2: Configure CodeLinks**

Create a file named ``src_trace.toml`` in your ``docs`` folder (next
to ``conf.py``) with the following content:

.. literalinclude:: ../../src_trace.toml
   :language: toml
   :caption: src_trace.toml

**Step 3: Add the src-trace Directive**

In your documentation files, add the following directive to display
traced source code links:

.. code-block:: rst

   .. src-trace::
        :project: x-as-code-cpp
        :directory: .

**Step 4: Annotate Your Source Code**

Add comments to your source code files to link code lines to needs.
For example, in ``src/main.cpp``:

.. literalinclude:: ../../../src/main.cpp
   :language: cpp
   :caption: src/main.cpp

**Step 5: View Traced Files and Lines**

After following the steps above, the documentation will show the
traced files and lines for each need in the specified project (``x-as-code-cpp``).
Here we show only the implementation files (not test files):

.. src-trace:: 
   :project: x-as-code-cpp
   :file: main.cpp

.. src-trace:: 
   :project: x-as-code-cpp
   :file: sample1.cpp

.. src-trace:: 
   :project: x-as-code-cpp
   :file: sample2.cpp

**Note**: Test files are traced separately in the :ref:`testing guide <testing>`
to avoid duplicate need IDs.

**Summary**

By following these steps, you can easily trace source code to
requirements, improving traceability and documentation quality.

Advanced configuration options and features are available in the `CodeLinks documentation <https://codelinks.useblocks.com/components/configuration.html>`__.

Linking Requirements to Code
----------------------------

Finally you can link from/to the traced source code lines like this:

.. req:: Requirement linking to source code
   :id: REQ_0815
   :status: open

   This is a requirement that links to a need that has traced source code
   lines.

.. note::

   Current limitation: ``ubCode`` is not aware of this need id yet. This
   means that the ``ubCode`` navigation inside Visual Studio Code will
   not work and jumping from this ``rst`` file to the source code line
   will not work. This will be implemented and supported in a future
   release.
