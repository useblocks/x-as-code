.. _external-needs:

:octicon:`link-external` How to integrate External Needs
========================================================

Sometimes you want to integrate needs from an external source into your documentation.
A known and valid use-case might be for example the integration of "plattform" requirements.

The following example shows how to integrate needs from an external json file.

.. code-block:: toml
    
    # file: ubproject.toml
    # docs/external/needs_external.json integration
    [[needs.external_needs]]
    json_path = "./external/needs_external.json"
    # use this to download from a remote
    # json_url = "https://sphinx-needs.readthedocs.io/en/latest/needs.json"
    base_url = "https://example.com"
    target_url = "{{need['id']}}"

External needs
--------------

Here are some needs that are external to the documentation,
but can still be linked by other needs in this documentation:

- :need:`REQ_1_1_ext`
- :need:`REQ_1_2_ext`
- :need:`SPEC_1_1_ext`
- :need:`SPEC_1_2_ext`

These external needs can be linked like normal needs:

.. req:: Requirement 1.1
   :id: REQ_1_1
   :status: open
   :links: REQ_1_1_ext

   This is a requirement that links to an external requirement.