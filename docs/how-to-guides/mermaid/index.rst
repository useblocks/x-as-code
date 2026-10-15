.. _mermaid-integration:

:octicon:`code-square` Mermaid Integration
==========================================

Mermaid is a popular tool for creating diagrams and visualizations using a simple markdown-like syntax. It is often used in documentation to illustrate concepts, workflows, and architectures.

The respective sphinx extension needs to be installed: `sphinxcontrib-mermaid <https://github.com/mgaitan/sphinxcontrib-mermaid>`_

.. caution::

    In some cases it is required to manually add the Mermaid javascript to the html static files. 
    In our case it is added in ``docs/_static/mermaid/mermaid.min.js``.

Sequence Diagram
----------------

.. mermaid::

   sequenceDiagram
      participant Alice
      participant Bob
      Alice->John: Hello John, how are you?
      loop Healthcheck
          John->John: Fight against hypochondria
      end
      Note right of John: Rational thoughts <br/>prevail...
      John-->Alice: Great!
      John->Bob: How about you?
      Bob-->John: Jolly good!

The same, but part of an architecture diagram need
--------------------------------------------------

This method allows to use the diagram inside a need and enables traceablility.

.. arch:: Mermaid inside architecture need
    :id: ARCH_004

    Another style ``forest`` is used here.

    .. mermaid::

        ---
        config:
          theme: 'forest'
        ---
        sequenceDiagram
          participant Alice
          participant Bob
          Alice->John: Hello John, how are you?
          loop Healthcheck
              John->John: Fight against hypochondria
          end
          Note right of John: Rational thoughts <br/>prevail...
          John-->Alice: Great!
          John->Bob: How about you?
          Bob-->John: Jolly good!