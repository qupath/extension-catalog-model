from pydantic import BaseModel, List, Optional, HttpUrl

class GitHubRepo(BaseModel):
    org: str
    repo: str

class QuPathVersions(BaseModel):
    min: str = "v0.6.0"
    max: Optional[str] = None

class GitHubRelease(BaseModel):
    name: str
    main_url: HttpUrl
    dependency_urls: Optional[List[HttpUrl]] = None
    qupath_compatible: QuPathVersions

class Extension(BaseModel):
    name: str
    description: str
    github: GitHubRepo
    versions: List[GitHubRelease]

