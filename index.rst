.. extension-catalog-model documentation master file, created by
   sphinx-quickstart on Mon Nov 11 11:30:45 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Extension catalog model documentation
=====================================

The extension catalog model is a `pydantic <https://docs.pydantic.dev/latest/>`_ model for creating, validating, reading and writing extension catalogs
for use with an `extension manager <https://github.com/qupath/extension-manager>`_.

To create a catalog:

* Create a GitHub repository.
* Add a `catalog.json` file to the repository.
* Write your catalog with the JSON format in `catalog.json` by following the specifications of :py:meth:`~extension_catalog_model.model.Catalog`.

An example can be found on the `QuPath catalog repository <https://github.com/qupath/qupath-catalog>`_.

Model specifications
====================

.. toctree::
   :maxdepth: 2

   autodocs
