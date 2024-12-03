from extension_index_model import VersionRange, Release, Extension, Index
import pytest

def test_version_ranges_can_be_created():
    v1 = VersionRange(min="v0.1.0")
    v2 = VersionRange(min="v0.1.0", max="v0.2.0")

def test_version_ranges_cant_be_disordered():
    with pytest.raises(Exception):
        VersionRange(min="v0.2.0", max="v0.1.0")

def test_version_excludes_cant_be_too_high():
    with pytest.raises(Exception):
        VersionRange(min="v0.2.0", max="v0.3.0", excludes=["v0.6.0"])

def test_version_excludes_cant_be_too_low():
    with pytest.raises(Exception):
        VersionRange(min="v0.2.0", max="v0.3.0", excludes=["v0.1.0"])

def test_release_can_be_created():
    Release(name="v0.1", main_url="https://github.com/a/b/", versions = VersionRange())

def test_release_needs_url():
    with pytest.raises(Exception):
        Release(name="v0.1", versions=VersionRange())

def test_release_url_must_match():
    with pytest.raises(Exception):
        Release(name="v0.1", main_url="https://github.com/", versions=VersionRange())

def test_release_url_must_be_gh():
    with pytest.raises(Exception):
        Release(name="v0.1", main_url="https://gitlab.com/a/b/", versions=VersionRange())

def test_release_needs_versions():
    with pytest.raises(Exception):
        Release(name="v0.1", main_url="https://github.com/a/b")

def test_required_deps_must_be_gh():
    Release(
        name="v0.1",
        main_url="https://github.com/a/b/", 
        required_dependency_urls=["https://github.com/a/b/"],
        versions=VersionRange())

def test_required_deps_must_be_gh():
    with pytest.raises(Exception):
        Release(
            name="v0.1",
            main_url="https://github.com/a/b/", 
            required_dependency_urls=["https://gitlab.com/a/b/"],
            versions=VersionRange())

def test_optional_deps():
    Release(
        name="v0.1",
        main_url="https://github.com/a/b/", 
        optional_dependency_urls=["https://github.com/a/b/"],
        versions=VersionRange())
        
def test_optional_deps_must_be_gh():
    with pytest.raises(Exception):
        Release(
            name="v0.1",
            main_url="https://github.com/a/b/", 
            optional_dependency_urls=["https://gitlab.com/a/b/"],
            versions=VersionRange())

def test_javadoc_urls():
    Release(
        name="foo",
        main_url="https://github.com/a/b/", 
        javadoc_urls=["https://github.com/a/b/"],
        versions=VersionRange())

def test_javadoc_urls_must_be_gh():
    with pytest.raises(Exception):
        Release(
            name="v0.1",
            main_url="https://github.com/a/b/", 
            javadoc_urls=["https://gitlab.com/a/b/"],
            versions=VersionRange())

def test_extension_creation():
    Extension(
        name="my-extension",
        description="My extension",
        author="Me",
        homepage="https://github.com/a/b",
        releases = [
            Release(
                name="v0.1",
                main_url="https://github.com/a/b/", 
                versions=VersionRange()
            )
        ]
    )

def test_extension_homepage_validation():
    with pytest.raises(Exception):
        Extension(
            name="my-extension",
            description="My extension",
            author="Me",
            homepage="https://github.com/",
            releases = [
                Release(
                    name="v0.1",
                    main_url="https://github.com/a/b/", 
                    versions=VersionRange()
                )
            ]
        )

def test_extension_homepage_must_be_gh():
    with pytest.raises(Exception):
        Extension(
            name="my-extension",
            description="My extension",
            author="Me",
            homepage="https://gitlab.com/a/b",
            releases = [
                Release(
                    name="v0.1",
                    main_url="https://github.com/a/b/", 
                    versions=VersionRange()
                )
            ]
        )

def test_index_creation():
    Index(
        name="My index",
        description="My description",
        extensions = [
            Extension(
                name="my-extension",
                description="My extension",
                author="Me",
                homepage="https://github.com/a/b",
                releases = [
                    Release(
                        name="v0.1",
                        main_url="https://github.com/a/b/", 
                        versions=VersionRange()
                    )
                ]
            )
        ]
    )


def test_index_cannot_have_duplicate_names():
    with pytest.raises(Exception):
        Index(
            name="My index",
            description="My description",
            extensions = [
                Extension(
                    name="my-extension",
                    description="My extension",
                    author="Me",
                    homepage="https://github.com/a/b",
                    releases = [
                        Release(
                            name="v0.1",
                            main_url="https://github.com/a/b/", 
                            versions=VersionRange()
                        )
                    ]
                ),
                Extension(
                    name="my-extension",
                    description="My extension",
                    author="Me",
                    homepage="https://github.com/a/b",
                    releases = [
                        Release(
                            name="v0.1",
                            main_url="https://github.com/a/b/", 
                            versions=VersionRange()
                        )
                    ]
                )
            ]
        )
