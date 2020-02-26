from pathlib import (
    Path as _Path,
)

from tasks.concepts import (
    Group as _Group,
    Semester as _Semester,
)

syllabus = {
    "ondisk": [],
    "parsed": {},
}

org_name = "ucfai"

semester = _Semester(shortname="sp20")
group = _Group("core", semester)

paths = {}
paths["disk"] = _Path(repr(group)) / repr(semester)
paths["repo"] = f"https://github.com/{org_name}/{str(paths['disk'])}"
paths["site"] = _Path("ucfai.org") / "content" / paths["disk"]

hugo = {
    "theme": "academic",
}

kaggle = {
    "username": "ucfaibot",
    "pulled": [],
}
