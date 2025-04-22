.. extension-catalog-model documentation master file, created by
   sphinx-quickstart on Mon Nov 11 11:30:45 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Extension catalog model documentation
=====================================

The extension catalog model is a `pydantic <https://docs.pydantic.dev/latest/>`_ model for creating, validating, reading and writing extension catalogs
for use with an `extension manager <https://github.com/qupath/extension-manager>`_.

To create a catalog, you can either use Python or QuPath:

* With Python:

   * Install this package:

   .. code-block:: bash

      pip install git+https://github.com/qupath/extension-catalog-model.git

   * Create and run a Python script that creates a `catalog.json` file with the JSON representation of a :py:meth:`~extension_catalog_model.model.Catalog`. A detailed description of each field of a catalog can be found on the specifications below.

   .. code-block:: python

      # create_catalog.py

      from extension_catalog_model.model import *

      version_range = VersionRange(min="v0.5.1")
      release = Release(
         name="v0.1.0-rc5",
         main_url="https://github.com/qupath/qupath-extension-omero/releases/download/v0.1.0-rc5/qupath-extension-omero-0.1.0-rc5.jar",
         optional_dependency_urls=["https://github.com/ome/openmicroscopy/releases/download/v5.6.14/OMERO.java-5.6.14-ice36.zip"],
         version_range=version_range
      )
      extension = Extension(
         name="QuPath OMERO extension",
         description="QuPath extension to work with images through OMERO's APIs",
         author="QuPath",
         homepage="https://github.com/qupath/qupath-extension-omero",
         releases=[release]
      )
      catalog = Catalog(
         name="QuPath catalog",
         description="Extensions maintained by the QuPath team",
         extensions=[extension]
      )

      with open("catalog.json", "w") as file:
         file.write(catalog.model_dump_json(indent=2))
         print(file.name + " written")

   .. code-block:: bash

      python3 create_catalog.py

* With QuPath v0.6 or later:

   * Open the script editor in QuPath (Automate -> Script editor).
   * Create and run a script that creates a `catalog.json` file with the JSON representation of a :py:meth:`~extension_catalog_model.model.Catalog`. A detailed description of each field of a catalog can be found on the specifications below.

   .. code-block:: java

      import qupath.ext.extensionmanager.core.catalog.*
      import com.google.gson.GsonBuilder
      import java.nio.file.Paths


      var versionRange = new VersionRange("v0.5.1", null, null)
      var release = new Release(
         "v0.1.0-rc5",
         new URI("https://github.com/qupath/qupath-extension-omero/releases/download/v0.1.0-rc5/qupath-extension-omero-0.1.0-rc5.jar"),
         null,
         List.of(new URI("https://github.com/ome/openmicroscopy/releases/download/v5.6.14/OMERO.java-5.6.14-ice36.zip")),
         null,
         versionRange
      )
      var extension = new Extension(
         "QuPath OMERO extension",
         "QuPath extension to work with images through OMERO's APIs",
         "QuPath",
         new URI("https://github.com/qupath/qupath-extension-omero"),
         false,
         List.of(release)
      )
      var catalog = new Catalog(
         "QuPath catalog",
         "Extensions maintained by the QuPath team",
         List.of(extension)
      )

      try (FileWriter fileWriter = new FileWriter("catalog.json")) {
         new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(catalog, fileWriter);
      }
      println "Catalog saved to " + Paths.get("catalog.json").toAbsolutePath()


Once the `catalog.json` file is created, create a GitHub repository and add `catalog.json` to the repository.

An example can be found on the `QuPath catalog repository <https://github.com/qupath/qupath-catalog>`_.

To read and validate a catalog from a file:

.. code-block:: python
   
   from extension_catalog_model.model import Catalog
   Catalog.parse_file("catalog.json")
   

Model specifications
====================

.. toctree::
   :maxdepth: 2

   autodocs
