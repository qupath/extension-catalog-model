from pydantic import BaseModel, HttpUrl
from pydantic.functional_validators import field_validator, model_validator
from packaging.version import Version

from typing import List, Optional
import re

class VersionRange(BaseModel):
    """
    A specification of the minimum and maximum versions that an extension supports. Versions should be specified in the form "v[MAJOR].[MINOR].[PATCH]" corresponding to semantic versions, although release candidate qualifiers (eg, "-rc1") are also allowed.

    :param min: The minimum/lowest version that this extension is known to be compatible with.
    :param max: The maximum/highest version that this extension is known to be compatible with.
    :param excludes: Any specific versions within the minimum and maximum range that are not compatible.
    """
    min: str = "v0.1.0"
    max: Optional[str] = None
    excludes: Optional[List[str]] = None

    @field_validator("min", "max")
    @classmethod
    def _validate_min(cls, min):
        return cls._validate_version(min)

    @model_validator(mode="after")
    def _validate_version_range(self):
        if (self.max is not None):
            vmin = Version(self.min)
            vmax = Version(self.max)
            assert vmin <= vmax, "Maximum version should be greater than or equal to minimum version."
            if self.excludes is not None:
                assert all([Version(x) <= vmax for x in self.excludes]), "All excludes entries should be between the minimum and maximum version."
        if self.excludes is not None:
            assert all([vmin <= Version(x) for x in self.excludes]), "All excludes entries should be between the minimum and maximum version."
        return self

    @classmethod
    def _validate_version(cls, version):
        return _validate_version(version)
    

    @field_validator("excludes")
    def _validate_excludes(cls, excludes):
        return [cls._validate_version(v) for v in excludes]
    
def _validate_version(version):
        assert re.match(r"^v[0-9]+\.[0-9]+\.[0-9]+(-rc[0-9]+)?$", version), "Versions should be specified in the form v[MAJOR].[MINOR].[PATCH] and may include pre-releases, eg v0.6.0-rc1."
        return version


class Release(BaseModel):
    """
    A description of an extension release hosted on GitHub.

    :param name: The name of the release. This should be a valid semantic version.
    :param main_url: The GitHub URL where the main extension jar or zip file can be downloaded.
    :param required_dependency_urls: SciJava Maven, Maven Central, or GitHub URLs where required dependency jars or zip files can be downloaded.
    :param optional_dependency_urls: SciJava Maven, Maven Central, or GitHub URLs where optional dependency jars or zip files can be downloaded.
    :param javadoc_urls: SciJava Maven, Maven Central, or GitHub URLs where javadoc jars or zip files can be downloaded.
    :param version_range: A specification of minimum and maximum compatible versions.
    """
    name: str
    main_url: HttpUrl
    required_dependency_urls: Optional[List[HttpUrl]] = None
    optional_dependency_urls: Optional[List[HttpUrl]] = None
    javadoc_urls: Optional[List[HttpUrl]] = None
    version_range: VersionRange

    @field_validator("name")
    @classmethod
    def _validate_name(cls, name):
        return _validate_version(name)

    @field_validator("main_url")
    @classmethod
    def _check_main_url(cls, main_url: HttpUrl):
        return _validate_primary_url(main_url)

    @field_validator("required_dependency_urls", 
    "optional_dependency_urls", "javadoc_urls")
    @classmethod
    def _check_urls(cls, urls):
        return [_validate_dependency_url(url) for url in urls]


class Extension(BaseModel):
    """
    A description of an extension.

    :param name: The extension's name.
    :param description: A short (one sentence or so) description of what the extension is and what it does.
    :param author: The author or group responsible for the extension.
    :param homepage: A link to the GitHub repository associated with the extension.
    :param releases: A list of available releases of the extension.
    """
    name: str
    description: str
    author: str
    homepage: HttpUrl
    releases: List[Release]
    
    @field_validator("homepage")
    @classmethod
    def _validate_homepage(cls, url):
        return _validate_primary_url(url)
    ## todo: should we check that the download links' owner/repo matches the homepage...?

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
    
    @field_validator("extensions")
    @classmethod
    def _validate_extension_list(cls, extensions):
        names = [ext.name for ext in extensions]
        assert len(names) == len(set(names)), "Duplicated extension names not allowed in extension index."
        return extensions

def _validate_primary_url(primary_url: HttpUrl):
    assert primary_url.scheme == "https", "URLs must use https"
    assert primary_url.host == "github.com", "Homepage and main download links must currently be hosted on github.com."
    assert re.match("^/[0-9a-zA-Z]+/[0-9a-zA-Z]+/?", primary_url.path) is not None, "Homepage and main download links must currently point to a valid github repo."
    return primary_url

def _validate_dependency_url(url):
    assert url.scheme == "https", "URLs must use https"
    assert url.host in ["github.com", "maven.scijava.org", "repo1.maven.org"], "Dependency and javadoc download links must currently be hosted on github.com, SciJava Maven, or Maven Central."
    return url
