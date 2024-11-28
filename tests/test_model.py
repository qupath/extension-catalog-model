from extension_index_model import VersionRange, Release, Extension, Index


def test_version_ranges_can_be_created():
    v1 = VersionRange(min="v0.1.0")
    v2 = VersionRange(min="v0.1.0", max="v0.2.0")

def test_version_ranges_cant_be_disordered():
    v2 = VersionRange(min="v0.2.0", max="v0.1.0")

def test_version_excludes_cant_be_too_high():
    v2 = VersionRange(min="v0.2.0", max="v0.3.0", excludes=["v0.6.0"])
def test_version_excludes_cant_be_too_low():
    v2 = VersionRange(min="v0.2.0", max="v0.3.0", excludes=["v0.1.0"])

def test_release_can_be_created():
    r = Release(name="foo", main_url="https://github.com", versions = VersionRange())
