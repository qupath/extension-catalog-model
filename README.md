# Extension catalog model

[![Coverage](https://qupath.github.io/badges/extension-catalog-model/badges/coverage-badge.svg?dummy=1234)](https://qupath.github.io/badges/extension-catalog-model/reports/coverage/index.html?dummy=1234)
[![Tests](https://qupath.github.io/badges/extension-catalog-model/badges/tests-badge.svg?dummy=1234)](https://qupath.github.io/badges/extension-catalog-model/reports/junit/report.html?dummy=1234)
![Actions](https://github.com/qupath/extension-catalog-model/actions/workflows/tests.yml/badge.svg?dummy=1234)

This is a [pydantic](https://docs.pydantic.dev/latest/) package for creating, validating and writing JSON files for the QuPath [extension manager](https://github.com/qupath/extension-manager) project.

Check out the [documentation](https://qupath.github.io/extension-catalog-model/) for guidance on creating a catalog.

To create a catalog:

```python
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
```

To read a catalog from a JSON file:

```python
from extension_catalog_model.model import Catalog
Catalog.parse_file("catalog.json")
```

An example can be found on the [QuPath catalog repository](https://github.com/qupath/qupath-catalog).
