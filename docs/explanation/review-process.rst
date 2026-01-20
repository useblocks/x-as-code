.. _review-process:

:octicon:`git-pull-request` The Review Process: From ALM to Git
===============================================================

.. note::

   **Target audience**: Engineers transitioning from ALM tools (Jama,
   Codebeamer, DOORS, Polarion) to code-based workflows with Git.

If you're coming from traditional Application Lifecycle Management (ALM) tools,
the way reviews work in Git-based platforms like GitHub, GitLab, and Bitbucket
might feel surprisingly simple. That's because it is.

ALM tools typically implement complex approval workflows with multiple stages,
role-based sign-offs, and elaborate configuration. Git platforms solved this
with a single, elegant concept: the **Pull Request** (or **Merge Request**).

----

Reviews in Traditional ALM Tools
--------------------------------

Traditional ALM tools approach reviews through formal workflow engines:

**State Machine Workflows**

Most ALM tools implement reviews as state transitions:

.. mermaid::

   stateDiagram-v2
       [*] --> Draft
       Draft --> InReview: Submit for Review
       InReview --> NeedsWork: Request Changes
       NeedsWork --> InReview: Resubmit
       InReview --> TechApproved: Technical Approval
       TechApproved --> SafetyReview: Route to Safety
       SafetyReview --> NeedsWork: Safety Concerns
       SafetyReview --> FinalApproval: Safety Sign-off
       FinalApproval --> Released: Management Approval
       Released --> [*]

**Characteristics of ALM Reviews**

* **Approval matrices** - Complex rules defining who must approve based on
  artifact type, classification, or affected system
* **Role-based sign-offs** - Different roles (author, reviewer, approver,
  release manager) with different permissions at each stage
* **Separate review comments** - Comments stored in the tool's database,
  often disconnected from the actual artifact content
* **Form-based transitions** - Moving between states requires filling forms,
  selecting reasons, or providing justifications
* **Configured workflows** - Each organization customizes state machines,
  leading to tool-specific complexity
* **Audit through the tool** - Change history lives in the ALM tool's
  proprietary database

While these features provide flexibility, they also introduce significant
overhead in configuration, training, and daily use.

----

How Git Platforms Solved This: Pull Requests
--------------------------------------------

Git-based platforms introduced a fundamentally simpler approach:
**propose changes in a branch, review them together, merge when approved**.

.. mermaid::

   flowchart LR
       A[Create Branch] --> B[Make Changes]
       B --> C[Open Pull Request]
       C --> D{Review}
       D --> |Request Changes| B
       D --> |Approve| E[Merge]
       E --> F[Changes in Main]

**The Pull Request Model**

A Pull Request (GitHub, Bitbucket) or Merge Request (GitLab) bundles everything
needed for review into one place:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - What It Does
   * - **Visual Diff**
     - Shows exactly what changed, line by line, with syntax highlighting
   * - **Inline Comments**
     - Comment directly on specific lines of code or content
   * - **Threaded Discussions**
     - Each comment thread can be resolved independently
   * - **Review States**
     - Three clear options: Approve, Request Changes, or Comment
   * - **Automatic Blocking**
     - Merge is blocked until required approvals are received
   * - **CI Integration**
     - Automated tests run on every change, results visible in PR

**Key Principles**

1. **Propose, don't commit directly** - Changes live in a branch until reviewed
   and approved. The main branch stays protected.

2. **Context is everything** - Reviewers see the exact changes alongside the
   discussion. No need to switch between tools or screens.

3. **Simple states** - No complex state machines. A PR is either open (needs
   work or review), approved (ready to merge), or merged (done).

4. **History in Git** - Every change, comment, and approval is part of the
   permanent Git history, not locked in a proprietary database.

----

Enforcing Reviews with CODEOWNERS
---------------------------------

But what about requiring specific people to review specific content? Git
platforms solve this with **CODEOWNERS** - a simple file that defines who
must approve changes to particular paths.

**How CODEOWNERS Works**

1. You create a ``CODEOWNERS`` file defining ownership patterns
2. When a PR touches files matching a pattern, owners are automatically
   requested as reviewers
3. Combined with branch protection rules, the PR cannot be merged until
   the designated owners approve

**Example CODEOWNERS File**

.. code-block:: text

   # Safety requirements need safety team approval
   /docs/requirements/safety/    @company/safety-team

   # Architecture changes need architect sign-off
   /docs/architecture/           @lead-architect

   # All requirement changes need requirements manager review
   /docs/requirements/           @requirements-manager

   # Hardware specs need hardware team approval
   /docs/specs/hardware/         @company/hw-engineers

**The Enforcement Flow**

.. mermaid::

   sequenceDiagram
       participant Dev as Developer
       participant PR as Pull Request
       participant CO as CODEOWNERS Check
       participant Owner as Code Owner
       participant Main as Main Branch

       Dev->>PR: Opens PR touching /docs/requirements/safety/
       PR->>CO: Checks CODEOWNERS file
       CO->>Owner: Requests review from @safety-team
       Note over PR: Merge blocked until approved
       Owner->>PR: Reviews changes
       Owner->>PR: Approves
       Note over PR: CODEOWNERS requirement satisfied
       Dev->>Main: Merges PR

**Enabling CODEOWNERS Enforcement**

To make CODEOWNERS reviews mandatory, combine with branch protection:

*GitHub:*

1. Go to **Settings > Branches > Branch protection rules**
2. Add rule for ``main``
3. Enable **Require pull request reviews before merging**
4. Enable **Require review from Code Owners**

*GitLab:*

1. Go to **Settings > Repository > Protected branches**
2. Configure protection for ``main``
3. Enable **Code owner approval** in merge request settings

.. seealso::

   For detailed CODEOWNERS configuration and additional access management
   strategies, see :ref:`access-management`.

----

ALM vs Git: Side-by-Side Comparison
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Aspect
     - Traditional ALM
     - Git-Based (PR/MR)
   * - **Where changes are made**
     - Directly in the tool's database
     - In a branch, proposed via PR
   * - **How reviews are requested**
     - Submit for review, enters workflow queue
     - Open a PR, assign reviewers or use CODEOWNERS
   * - **Where comments live**
     - Tool's comment database
     - Inline on the diff, part of PR history
   * - **How approval is given**
     - State transition with sign-off form
     - Click "Approve" on the PR
   * - **Review visibility**
     - Often requires navigating to review section
     - All visible in one PR page with full diff
   * - **Change history**
     - Proprietary audit log
     - Git history + PR conversation history
   * - **CI/CD integration**
     - Often requires separate configuration
     - Built-in: checks run automatically on PRs
   * - **Enforcing specific reviewers**
     - Approval matrix configuration
     - CODEOWNERS file + branch protection

----

Platform Features Comparison
----------------------------

All major Git platforms support the Pull Request review model with slight
variations:

.. list-table::
   :header-rows: 1
   :widths: 30 23 23 24

   * - Feature
     - GitHub
     - GitLab
     - Bitbucket
   * - **PR/MR Name**
     - Pull Request
     - Merge Request
     - Pull Request
   * - **Required Approvals**
     - Yes (branch rules)
     - Yes (approval rules)
     - Yes (merge checks)
   * - **CODEOWNERS**
     - Yes
     - Yes (CODEOWNERS file)
     - Yes (via default reviewers)
   * - **Draft PRs/MRs**
     - Yes
     - Yes
     - Yes
   * - **Auto-assign Reviewers**
     - Yes
     - Yes (reviewer roulette)
     - Yes
   * - **CI Status Checks**
     - GitHub Actions
     - GitLab CI
     - Bitbucket Pipelines
   * - **Merge Blocking**
     - Branch protection
     - Protected branches
     - Branch permissions
   * - **Inline Suggestions**
     - Yes
     - Yes
     - Yes

----

Benefits Summary
----------------

For engineers coming from ALM tools, the Git-based review model offers:

**Transparency**
   All changes visible in one place. No hunting through different tool
   sections to understand what's being proposed.

**Context**
   Reviewers see the exact changes with syntax highlighting, not abstract
   descriptions or change summaries.

**Efficiency**
   No separate forms, status transitions, or workflow configurations.
   Open a PR, get reviews, merge.

**Traceability**
   Complete history in Git. Every change is attributed, timestamped,
   and linked to the discussion that approved it.

**Automation**
   CI/CD pipelines run automatically on every PR. Tests, builds, and
   validations happen without manual triggers.

**Portability**
   Your review history travels with your Git repository. No vendor
   lock-in to proprietary audit databases.

----

.. seealso::

   * :ref:`access-management` - Strategies for access control including
     detailed CODEOWNERS configuration
   * :ref:`gh-actions-build` - Setting up CI/CD with GitHub Actions
