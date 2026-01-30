.. _testing:

:octicon:`beaker` Test Management and Traceability
==================================================

.. toctree:: requirements
   :maxdepth: 1
   :hidden:

This guide demonstrates how to integrate test reports into your
documentation with full traceability between test specifications, test
cases, source code, and test results.

Overview
--------

A comprehensive testing approach includes:

* **Test Specifications**: Define what needs to be tested
* **Test Cases**: Actual test implementations in code
* **Source Code**: The implementation being tested
* **Traceability**: Links between all these elements
* **Test Reports**: Results from test execution

By using Sphinx-Needs for test specifications, sphinx-codelinks for
code tracing, and sphinx-test-reports for test results, we create a
complete traceable testing ecosystem.

Workflow
--------

.. mermaid:: 

   graph LR
      REQ[Requirements] --> TS[Test Specifications]
      TS --> TC[Test Cases in Code]
      TC --> IMPL[Implementation Code]
      TC --> RUN[Test Execution]
      RUN --> REPORT[Test Reports]
      REPORT --> DOC[Documentation]

      style REQ fill:#FFB300
      style TS fill:#A6BDD7
      style TC fill:#A6BDD7
      style IMPL fill:#fa8638
      style REPORT fill:#4aac73
      style DOC fill:#F6768E

Step 1: Define Test Specifications
----------------------------------

Create test specifications using the ``test-spec`` directive to define
what needs to be tested:

.. test-spec:: Factorial Function Test Specification
   :id: TS_FACTORIAL
   :status: open
   :tags: factorial, math

   Test the factorial function for:

   * Negative numbers (should return 1)
   * Zero (should return 1)
   * Positive numbers (should return correct factorial)

   The factorial function is critical for mathematical operations and
   must handle edge cases correctly.

.. test-spec:: Prime Number Check Test Specification
   :id: TS_PRIME
   :status: open
   :tags: prime, math

   Test the IsPrime function for:

   * Negative numbers (should return false)
   * Trivial cases (0, 1, 2, 3)
   * Positive numbers (both prime and composite)

   Prime number detection is used in cryptographic operations and must be
   accurate.

Step 2: Annotate Test Cases in Code
-----------------------------------

Add sphinx-codelinks annotations to your test cases. The annotation
format is e.g.:

.. code-block:: cpp

   // @<description>, <need_id>, <need_type>
   TEST(TestSuite, TestName) {
       // test implementation
   }

Example from ``sample1_unittest.cpp``:

.. literalinclude:: ../../../src/sample1_unittest.cpp
   :language: cpp
   :lines: 76-88
   :caption: Annotated test case with GTest properties

The annotation ``@Test negative factorial values, T_FACT_001, test``
creates a traceable link between the test code and the documentation.

**GTest Properties** (``RecordProperty``):

* ``need_id``: Links the test execution result to the test case need
  (T_FACT_001)
* ``requirement``: Links to the requirement being tested (REQ_MATH_001)
* ``test_spec``: Links to the test specification (TS_FACTORIAL)

These properties are included in the XML test report and enable
automatic linking between test results and documentation needs.

Step 3: Link Test Cases to Specifications
-----------------------------------------

Test cases are automatically discovered from source code using
sphinx-codelinks. The test files contain ``@`` annotations that define
test needs:

.. code-block:: cpp

   // @Test negative factorial values, T_FACT_001, test
   TEST(FactorialTest, Negative) {
     RecordProperty("need_id", "T_FACT_001");
     RecordProperty("requirement", "REQ_MATH_001");
     RecordProperty("test_spec", "TS_FACTORIAL");
     // ... test implementation
   }

These annotations are parsed by sphinx-codelinks and automatically
create test needs. Below are all test cases discovered from the test
files:

.. src-trace:: 
   :project: x-as-code-cpp
   :file: sample1_unittest.cpp

The test cases link to:

* **Test specifications** (e.g., ``TS_FACTORIAL``) via the ``:spec:``
  field
* **Implementation** (e.g., ``IMPL_2``) via the ``:implements:`` field
* **Requirements** (e.g., ``REQ_MATH_001``) via GTest properties

Step 4: Show Code Traceability
------------------------------

Use sphinx-codelinks to display where test cases are implemented:

.. code-block:: rst

   .. src-trace:: Test Case Implementation
       :project: x-as-code-cpp
       :directory: src

This shows all annotated code locations, creating bidirectional links
between documentation and source code.

Step 5: Integrate Test Reports
------------------------------

After running tests, integrate the test results using
sphinx-test-reports:

.. code-block:: bash

   # Build and run tests
   cd src
   cmake -S . -B build
   cmake --build build
   cd build
   ./eac_test --gtest_output=xml:test-results.xml

The test results XML file contains properties that link back to the
test case needs, enabling complete traceability.

Traceability Matrix
-------------------

Test Specifications to Test Cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

View which test cases implement each test specification:

.. needtable::
   :filter: "TS_" in id or "T_" in id
   :columns: id, title, type, status, spec, implements
   :style: table

Test Cases to Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

View the connection between test cases and the code they test:

.. needflow::
   :filter: "T_" in id or "IMPL_" in id
   :show_link_names:

Coverage Analysis
-----------------

To generate code coverage reports with line-level detail:

.. code-block:: bash

   # Run tests with coverage
   ./scripts/test_with_coverage.sh

   # View coverage report
   open src/build/coverage_html/index.html

The coverage report shows:

* **Line Coverage**: Which lines of code were executed during tests
* **Function Coverage**: Which functions were called
* **Branch Coverage**: Which conditional branches were taken

CI/CD Integration
-----------------

Integrate testing into your CI/CD pipeline:

.. code-block:: yaml

   # .github/workflows/test.yml
   - name: Build C++ Project
     run: |
       cd src
       cmake -S . -B build
       cmake --build build

   - name: Run Tests
     run: |
       cd src/build
       ./eac_test --gtest_output=xml:test-results.xml

   - name: Upload Test Results
     uses: actions/upload-artifact@v4
     with:
       name: test-results
       path: src/build/test-results.xml

Complete Traceability Flow
--------------------------

The complete flow from requirements to test results:

.. needflow::
   :filter: "REQ_" in id or "TS_" in id or "T_" in id or "IMPL_" in id
   :show_link_names:
   :show_legend:

This visualization shows:

* Requirements drive test specifications
* Test specifications lead to test cases
* Test cases verify implementations
* Everything is traceable and documented

Summary
-------

By combining:

* **Sphinx-Needs**: For requirements and test specifications
* **Sphinx-Codelinks**: For linking documentation to source code
* **Sphinx-Test-Reports**: For integrating test execution results

You create a fully traceable testing ecosystem where:

✅ Every test links to its specification ✅ Every test links to the
code it verifies ✅ Test results are automatically integrated ✅
Coverage is measured and reported ✅ Traceability is bidirectional and
complete

Additional Resources
--------------------

* `GoogleTest Documentation <https://google.github.io/googletest/>`_
* `Sphinx-Test-Reports <https://sphinx-test-reports.readthedocs.io/>`_
* `Sphinx-Codelinks <https://codelinks.useblocks.com/>`_
* `Code Coverage with lcov <https://github.com/linux-test-project/lcov>`_
