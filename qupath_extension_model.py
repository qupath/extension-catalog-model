from pydantic import BaseModel, List, Optional, HttpUrl

class QuPathVersionRange(BaseModel):
    min: str = "v0.6.0"
    max: Optional[str] = None

class Release(BaseModel):
    name: str
    main_url: HttpUrl
    dependency_urls: Optional[List[HttpUrl]] = None
    qupath_compatible: QuPathVersionRange

class Extension(BaseModel):
    name: str
    description: str
    homepage: HttpUrl
    versions: List[Release]

class Index(BaseModel):
    name: str
    description: str
    extensions: List[Extension]
