from pydantic import BaseModel, HttpUrl, field_validator

from typing import List, Optional
import re

class VersionRange(BaseModel):
    """
    A specification of the minimum and maximum versions that an extension supports. Versions should be specified in the form "v[MAJOR].[MINOR].[PATCH]" corresponding to semantic versions.

    :param min: The minimum/lowest version that this extension is known to be compatible with.
    :param max: The maximum/highest version that this extension is known to be compatible with.
    :param excludes: Any specific versions that are not compatible.
    """
    min: str = "v0.6.0"
    max: Optional[str] = None
    excludes: Optional[str] = None

    @field_validator("min", "max")
    def _validate_version(cls, version):
        assert re.match("^v\d+\.\d+\.\d+(-rc\d+)?$", version), "Versions should be specified in the form v[MAJOR].[MINOR].[PATCH] and may include pre-releases, eg v0.6.0-rc1"
        return version

    @field_validator("excludes")
    def _validate_excludes(cls, excludes):
        return [cls._validate_version(v) for v in excludes]

class Release(BaseModel):
    """
    A description of an extension release hosted on GitHub.

    :param name: The name of the release.
    :param main_url: The GitHub URL where the main extension jar can be downloaded.
    :param dependency_urls: SciJava Maven, Maven Central, or GitHub URLs where dependency jars can be downloaded.
    :param javadoc_urls: SciJava Maven, Maven Central, or GitHub URLs where javadoc jars for the main extension jar and for dependencies can be downloaded.
    :param versions: A specification of minimum and maximum compatible versions.
    """
    name: str
    main_url: HttpUrl
    dependency_urls: Optional[List[HttpUrl]] = None
    javadoc_urls: Optional[List[HttpUrl]] = None
    versions: VersionRange

    @field_validator("main_url")
    def _check_main_url(cls, main_url: HttpUrl):
        return _validate_primary_url(main_url)

    @field_validator("dependency_urls", "javadoc_urls")
    def _check_urls(cls, urls):
        return [cls._check_maven_or_github_url(cls, url) for url in urls]

    def _check_maven_or_github_url(cls, url):
        assert url.host in ["github.com", "maven.scijava.org", "repo1.maven.org"], "Dependency and javadoc download links must currently be hosted on github.com, SciJava Maven, or Maven Central"
        return url


class Extension(BaseModel):
    """
    A description of an extension.

    :param name: The extension's name.
    :param description: A short (one sentence or so) description of what the extension is and what it does.
    :param author: The author or group responsible for the extension.
    :param homepage: A link to the GitHub repository associated with the extension.
    :param versions: A list of available versions of the extension.
    """
    name: str
    description: str
    author: str
    homepage: HttpUrl
    versions: List[Release]
    
    @field_validator("homepage")
    def _validate_homepage(cls, url):
        _validate_primary_url(url)

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

def _validate_primary_url(primary_url: HttpUrl):
    assert primary_url.host == "github.com", "Homepage and main download links must currently be hosted on github.com"
    return primary_url
