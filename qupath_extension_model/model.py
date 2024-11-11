from pydantic import BaseModel, HttpUrl

from typing import List, Optional


class QuPathVersionRange(BaseModel):
    """
    A specification of the minimum and maximum QuPath versions that an extension supports. Versions should be specified in the form "v[MAJOR].[MINOR].[PATCH]" corresponding to QuPath semantic versions. Release candidates should not be included.

    :param min: The minimum/lowest QuPath version that this extension is known to be compatible with.
    :param max: The maximum/highest QuPath version that this extension is known to be compatible with.
    :param excludes: Any specific versions that are not compatible.
    """
    min: str = "v0.6.0"
    max: Optional[str] = None
    excludes: Optional[str] = None

class Release(BaseModel):
    """
    A description of an extension release hosted on GitHub.

    :param name: The name of the release.
    :param main_url: The GitHub URL where the main extension jar can be downloaded.
    :param dependency_urls: SciJava Maven, Maven Central, or GitHub URLs where dependency jars can be downloaded.
    :param javadoc_urls: SciJava Maven, Maven Central, or GitHub URLs where javadoc jars for the main extension jar and for dependencies can be downloaded.
    :param qupath_versions: A specification of minimum and maximum compatible QuPath versions.
    """
    name: str
    main_url: HttpUrl
    dependency_urls: Optional[List[HttpUrl]] = None
    javadoc_urls: Optional[List[HttpUrl]] = None
    qupath_versions: QuPathVersionRange

class Extension(BaseModel):
    """
    A description of an extension.

    :param name: The extension's name.
    :param description: A short (one sentence or so) description of what the extension is and what it does.
    :param homepage: A link to the GitHub repository associated with the extension.
    :param versions: A list of available versions of the extension.
    """
    name: str
    description: str
    homepage: HttpUrl
    versions: List[Release]

class Index(BaseModel):
    """
    An index describing a collection of extensions.

    :param name: The name of the index.
    :param description: A short (one sentence or so) description of what the index contains and what its purpose is.
    :param extensions: The collection of extensions that the index describes.
    """
    name: str
    description: str
    extensions: List[Extension]
