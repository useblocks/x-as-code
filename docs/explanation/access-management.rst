.. _access-management:

:octicon:`lock` Access Management Strategies
============================================

.. note::

   **Target audience**: Engineers transitioning from ALM tools (Jama,
   Codebeamer, DOORS) to code-based requirements management with
   sphinx-needs.

Traditional Application Lifecycle Management (ALM) tools like Jama, Codebeamer,
and IBM DOORS provide sophisticated built-in access management. These tools offer:

* **Role-based permissions** - Define who can read, edit, or approve specific requirement types
* **Field-level access** - Control visibility of sensitive attributes
* **Approval workflows** - Require sign-off from designated reviewers
* **Audit trails** - Track every change with user attribution

When transitioning to code-based requirements management with sphinx-needs,
this built-in access control disappears. Repository access typically means
access to everything within that repository.

This chapter explores strategies to achieve similar access control objectives
within a code-based workflow.

----

The Access Control Paradigm Shift
---------------------------------

The fundamental difference between ALM tools and code-based requirements
management lies in how access control is enforced:

**ALM Model**: The tool acts as gatekeeper

.. mermaid::

   flowchart LR
       U[User] --> |"Permission Check"| T[ALM Tool]
       T --> |"Allowed?"| D[Requirements Data]

**Code-Based Model**: Version control + review workflows

.. mermaid::

   flowchart LR
       U[User] --> R[Repository]
       R --> |"PR Review"| M[Merge Gate]
       M --> D[Requirements Data]

The key insight is that **control shifts from "who can edit" to "what gets merged"**.
In the ALM world, the tool prevents unauthorized changes. In the code-based world,
anyone with repository access can propose changes, but review workflows and
automation determine what actually makes it into the main branch.

This shift brings benefits:

* **Transparency** - All changes are visible in version control history
* **Collaboration** - Easier to propose and discuss changes
* **Auditability** - Git provides a complete change log

But also challenges:

* **No built-in field-level security** - Repository access = access to all content
* **Different mental model** - Engineers must adapt their expectations

----

Strategy 1: Git Submodules
--------------------------

**Concept**: Use separate repositories with different access permissions,
then include them as submodules in your main documentation project.

**Use case**: Hardware requirements managed by the hardware team,
safety requirements managed by the safety team, each in their own
access-controlled repository.

Setting Up Submodules
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Add a submodule for hardware requirements
   git submodule add git@github.com:company/hw-requirements.git docs/external/hw-reqs

   # Add a submodule for safety requirements (restricted access)
   git submodule add git@github.com:company/safety-requirements.git docs/external/safety-reqs

   # Initialize and update submodules
   git submodule update --init --recursive

Repository Structure
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   my-project/
   ├── docs/
   │   ├── requirements/           # Your team's requirements
   │   │   └── software.rst
   │   ├── external/
   │   │   ├── hw-reqs/            # Submodule (HW team owns)
   │   │   │   └── hardware.rst
   │   │   └── safety-reqs/        # Submodule (Safety team owns)
   │   │       └── safety.rst
   │   └── conf.py
   ├── .gitmodules
   └── ubproject.toml

Linking Across Submodules
~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx-needs allows linking to needs defined in submodule documentation:

.. code-block:: rst

   .. req:: Software shall interface with hardware
      :id: SW_REQ_001
      :links: HW_REQ_042

   This requirement implements hardware interface requirement
   :need:`HW_REQ_042`.

Evaluation
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Evaluation
   * - Access Control
     - **Strong** - Each repo has independent permissions
   * - Complexity
     - Medium - Submodule management adds overhead
   * - Traceability
     - Full - Needs can link across submodules
   * - Real-time Updates
     - Manual - Requires explicit submodule update

----

Strategy 2: CODEOWNERS
----------------------

**Concept**: Use platform-native CODEOWNERS files to require reviews
from specific teams before changes can be merged.

**Use case**: All requirement changes must be approved by the requirements
manager; safety-critical requirements need safety team sign-off.

.. important::

   CODEOWNERS does not prevent viewing - it enforces review requirements
   before merge. Combine with branch protection rules for effectiveness.

CODEOWNERS File
~~~~~~~~~~~~~~~

Create ``.github/CODEOWNERS`` (GitHub) or ``CODEOWNERS`` in the repository root (GitLab):

.. code-block:: text

   # Safety requirements require safety team approval
   /docs/requirements/safety/    @company/safety-team

   # Hardware interface specs require HW team approval
   /docs/specs/hardware/         @company/hw-engineers

   # Architecture decisions need architect review
   /docs/architecture/           @lead-architect @company/architects

   # All requirement changes need requirements manager
   /docs/requirements/           @requirements-manager

Branch Protection Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combine CODEOWNERS with branch protection rules:

**GitHub:**

1. Navigate to repository **Settings > Branches**
2. Add rule for ``main`` branch
3. Enable **Require pull request reviews before merging**
4. Enable **Require review from Code Owners**
5. Set minimum number of approving reviews

**GitLab:**

1. Navigate to **Settings > Repository > Protected branches**
2. Configure ``main`` branch protection
3. Set **Allowed to merge** and **Allowed to push** appropriately
4. Enable **Code owner approval** in merge request settings

Evaluation
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Evaluation
   * - Access Control
     - **Review-based** - Cannot prevent read access
   * - Complexity
     - Low - Simple file-based configuration
   * - Traceability
     - Maintained - Standard PR workflow
   * - Auditability
     - Good - PR history shows all approvals

----

Strategy 3: Release Artifacts and needimport
--------------------------------------------

**Concept**: Build requirements documentation separately, publish the
``needs.json`` as a release artifact, and import it in consumer repositories
using sphinx-needs external needs feature.

**Use case**: A platform team publishes interface requirements that
multiple product teams consume without needing access to the source.

Producer: Publish needs.json
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure the producer project to export needs:

.. code-block:: toml

   # file: ubproject.toml
   [needs]
   build_json = true

In your CI/CD pipeline, publish ``_build/html/needs.json`` as a release artifact:

.. code-block:: yaml

   # file: .github/workflows/publish-needs.yml
   name: Publish Requirements
   on:
     release:
       types: [published]

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Build documentation
           run: |
             pip install sphinx sphinx-needs
             sphinx-build -b html docs docs/_build/html

         - name: Upload needs.json to release
           uses: softprops/action-gh-release@v1
           with:
             files: docs/_build/html/needs.json

Consumer: Import External Needs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure the consumer project to import the published needs:

.. code-block:: toml

   # file: ubproject.toml

   [[needs.external_needs]]
   # Download from release artifact
   json_url = "https://github.com/company/platform-requirements/releases/latest/download/needs.json"
   base_url = "https://company.github.io/platform-requirements"
   target_url = "{{need['docname']}}.html#{{need['id']}}"

Or download in CI and use a local path:

.. code-block:: toml

   [[needs.external_needs]]
   json_path = "./external/platform_needs.json"
   base_url = "https://company.github.io/platform-requirements"
   target_url = "{{need['docname']}}.html#{{need['id']}}"

Linking to External Needs
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. req:: Product shall use platform authentication
      :id: PROD_REQ_001
      :links: PLAT_AUTH_001

   This requirement implements platform requirement :need:`PLAT_AUTH_001`
   from the platform team.

Workflow Overview
~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant PT as Platform Team Repo
       participant CI as CI/CD Pipeline
       participant GH as GitHub Releases
       participant PR as Product Team Repo

       PT->>CI: Push/Tag release
       CI->>CI: Build sphinx docs
       CI->>GH: Publish needs.json artifact
       PR->>GH: Fetch needs.json
       PR->>PR: Build with external_needs
       Note over PR: Links resolve to platform docs

Evaluation
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Evaluation
   * - Access Control
     - **Strong** - Source access completely isolated
   * - Complexity
     - Medium - Requires CI/CD setup
   * - Traceability
     - Full - Links work across projects
   * - Real-time Updates
     - Periodic - Based on release cadence

----

Strategy 4: Copybara
--------------------

**Concept**: Use Google's Copybara tool to synchronize requirements between
repositories with transformations that can filter or modify content during sync.

**Use case**: Internal requirements repository synced to an external-facing
repository with sensitive fields (contacts, internal notes) removed.

.. tip::

   Copybara is particularly powerful when you need to share some requirements
   externally but keep certain metadata internal.

Copybara Configuration
~~~~~~~~~~~~~~~~~~~~~~

Create ``copy.bara.sky`` in your repository:

.. code-block:: python

   core.workflow(
       name = "sync-requirements",
       origin = git.origin(
           url = "git@internal.company.com:requirements/internal.git",
           ref = "main",
       ),
       destination = git.destination(
           url = "git@github.com:company/public-requirements.git",
           fetch = "main",
           push = "main",
       ),
       # Only sync the requirements directory
       origin_files = glob(["docs/requirements/**"]),

       authoring = authoring.overwrite(
           "Requirements Bot <requirements-bot@company.com>"
       ),

       transformations = [
           # Remove internal contact information
           core.replace(
               before = ":internal_contact: ${contact}",
               after = "",
               regex_groups = {"contact": ".*"},
               paths = glob(["**/*.rst"]),
           ),
           # Remove internal notes sections
           core.replace(
               before = ".. internal-note::\n${content}",
               after = "",
               regex_groups = {"content": "(?s).*?(?=\n\n|$)"},
               multiline = True,
               paths = glob(["**/*.rst"]),
           ),
           # Exclude confidential directories entirely
           core.filter_exclude(
               paths = glob(["**/confidential/**", "**/internal/**"]),
           ),
       ],
   )

Running Copybara
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # One-time sync
   copybara copy.bara.sky sync-requirements

   # In CI/CD - sync on every push to main
   copybara copy.bara.sky sync-requirements --git-destination-non-fast-forward

Evaluation
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Evaluation
   * - Access Control
     - **Strong** - Can filter sensitive content during sync
   * - Complexity
     - High - Requires Copybara infrastructure and maintenance
   * - Flexibility
     - Excellent - Arbitrary transformations possible
   * - Maintenance
     - Medium - Transformation rules need updates when format changes

----

Strategy 5: Branch Protection and CI Validation
-----------------------------------------------

**Concept**: Use branch protection rules and CI validation as complementary
controls that work alongside other strategies.

.. note::

   These controls work best in combination with other strategies like
   CODEOWNERS, not as standalone access management.

Branch Protection Rules
~~~~~~~~~~~~~~~~~~~~~~~

Configure branch protection to enforce quality gates:

* Require pull request before merging
* Require status checks to pass (CI validation)
* Require signed commits for compliance
* Restrict who can push to protected branches

Pre-commit Hooks
~~~~~~~~~~~~~~~~

Use pre-commit hooks for local validation before push.

**Using ubCode (ubc)**

The recommended approach is to use `ubCode <https://ubcode.useblocks.com>`_ (``ubc``),
the Sphinx-Needs companion CLI that provides built-in validation:

.. code-block:: yaml

   # file: .pre-commit-config.yaml
   repos:
     - repo: local
       hooks:
         - id: ubc-check
           name: Validate Sphinx-Needs with ubCode
           entry: ubc check docs/
           language: system
           files: '\.rst$'
           pass_filenames: false

``ubc check`` validates:

* Need ID uniqueness and format
* Required fields and attributes
* Link integrity between needs
* Schema compliance (when configured)

**Custom Validation Scripts**

Alternatively, use custom Python scripts for specific validation rules:

.. code-block:: yaml

   # file: .pre-commit-config.yaml
   repos:
     - repo: local
       hooks:
         - id: validate-requirements
           name: Validate requirement IDs
           entry: python scripts/validate_needs.py
           language: python
           files: '^docs/requirements/.*\.rst$'

         - id: check-need-links
           name: Check need links are valid
           entry: python scripts/check_links.py
           language: python
           files: '\.rst$'

CI Validation
~~~~~~~~~~~~~

Use CI to enforce constraints that complement access control.

**Using ubc-action**

The `ubc-action <https://github.com/useblocks/ubc-action>`_ provides a GitHub Action
to run ubCode validation in your CI pipeline:

.. code-block:: yaml

   # file: .github/workflows/validate-requirements.yml
   name: Validate Requirements
   on: [pull_request]

   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Setup ubCode
           uses: useblocks/ubc-action@v1
           with:
             license-key: ${{ secrets.UBCODE_LICENSE_KEY }}
             license-user: ${{ secrets.UBCODE_LICENSE_USER }}

         - name: Validate requirements with ubCode
           run: ubc check docs/

         - name: Build documentation (strict mode)
           run: |
             pip install sphinx sphinx-needs
             sphinx-build -W -b html docs docs/_build/html

.. tip::

   For a complete example of a documentation build workflow with GitHub Actions,
   see this repository's workflow in ``.github/workflows/gh_pages.yml`` or view it on
   `GitHub <https://github.com/useblocks/x-as-code/blob/main/.github/workflows/gh_pages.yml>`_.

**Custom Validation Scripts**

For additional validation beyond what ubCode provides:

.. code-block:: yaml

   # file: .github/workflows/validate-requirements.yml
   name: Validate Requirements
   on: [pull_request]

   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - name: Build documentation (strict mode)
           run: |
             pip install sphinx sphinx-needs
             sphinx-build -W -b html docs docs/_build/html

         - name: Validate need constraints
           run: |
             # Check all requirements have required fields
             python scripts/check_constraints.py docs/_build/html/needs.json

         - name: Check for forbidden patterns
           run: |
             # Ensure no internal-only markers in public docs
             ! grep -r "INTERNAL_ONLY" docs/requirements/

Evaluation
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Evaluation
   * - Access Control
     - **Complementary** - Enforces quality, not access
   * - Complexity
     - Low to Medium - Standard DevOps practices
   * - Automation
     - Excellent - Catches issues automatically
   * - Coverage
     - Good - Validates on every change

----

Enterprise Solution: ubTrace
----------------------------

For organizations with enterprise-grade access management requirements,
`ubTrace <https://useblocks.com>`_ from useblocks provides comprehensive
access control as a managed solution.

Features
~~~~~~~~

* **Role-based access control** - Define permissions at artifact level
* **Real-time traceability dashboard** - Visual relationship mapping across all artifacts
* **Audit logging** - Complete change history with user attribution
* **Multi-tool integration** - Connect DOORS, Polarion, Codebeamer, Jira
* **Historical tracking** - Trend analysis and time-based comparisons

When to Consider ubTrace
~~~~~~~~~~~~~~~~~~~~~~~~

* **Compliance requirements** - Industries with strict audit requirements (automotive, aerospace, medical)
* **Multi-tool workflows** - Need to integrate sphinx-needs with existing ALM tools
* **Enterprise scale** - Large organizations with complex permission requirements
* **Managed solution** - Prefer commercial support over DIY approaches

ubTrace is part of the useblocks commercial offering alongside
`ubConnect <https://useblocks.com>`_ for ALM data synchronization and
`ubCode <https://useblocks.com>`_ for VS Code integration.

.. seealso::

   Contact useblocks for enterprise requirements management solutions:
   https://useblocks.com

----

Choosing the Right Strategy
---------------------------

Decision Matrix
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 14 12 12 12 32

   * - Strategy
     - Access Control
     - Complexity
     - Real-time
     - Cost
     - Best For
   * - Git Submodules
     - Strong
     - Medium
     - Manual
     - Free
     - Multi-team with separate repo ownership
   * - CODEOWNERS
     - Review-based
     - Low
     - Yes
     - Free
     - Approval workflows within single repo
   * - Release Artifacts
     - Source isolated
     - Medium
     - Periodic
     - Free
     - Publishing requirements to consumers
   * - Copybara
     - Strong + filter
     - High
     - Configurable
     - Free
     - Content transformation during sync
   * - Branch + CI
     - Complementary
     - Low
     - Yes
     - Free
     - Quality enforcement (use with others)
   * - ubTrace
     - Full RBAC
     - Low (managed)
     - Yes
     - Commercial
     - Enterprise compliance

Decision Flowchart
~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
       A[Need access control?] --> |Yes| B{Enterprise compliance?}
       A --> |No| Z[Standard workflow with CODEOWNERS]
       B --> |Yes| C[ubTrace]
       B --> |No| D{Multiple teams/repos?}
       D --> |Same repo| E[CODEOWNERS + Branch Protection]
       D --> |Different repos| F{Need source isolation?}
       F --> |Yes| G{Need filtering?}
       F --> |No| H[Git Submodules]
       G --> |Yes| I[Copybara]
       G --> |No| J[Release Artifacts + needimport]

----

Summary
-------

Key takeaways for access management in code-based requirements:

1. **Paradigm shift**: Control moves from "who can edit" to "what gets merged"

2. **Layer your strategies**: Combine CODEOWNERS with branch protection
   for defense in depth

3. **Match strategy to need**:

   * Same repo, different teams: **CODEOWNERS**
   * Different repos, full access needed: **Git Submodules**
   * Publish/consume pattern: **Release artifacts + needimport**
   * Content filtering needed: **Copybara**
   * Enterprise compliance: **ubTrace**

4. **Audit trail**: Git history + PR reviews provide comprehensive traceability

5. **Start simple**: Begin with CODEOWNERS and branch protection,
   add complexity only when needed

.. seealso::

   * :ref:`external-needs` - How to integrate external needs
   * :ref:`gh-actions-build` - GitHub Actions integration
   * `Sphinx-Needs External Needs <https://sphinx-needs.readthedocs.io/en/latest/configuration.html#needs-external-needs>`_
   * :ref:`reference` - Tool overview including ubConnect and ubTrace
