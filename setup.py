from setuptools import setup, find_packages
from typing import Any, Dict
from yaml import FullLoader, load

package_info: Dict[str, Any]
with open("package-info.yml", "r") as info:
	package_info = load(info.read(), Loader=FullLoader)

description: str
with open("README.md", "r") as desc:
	description = desc.read()

development_status = int(package_info.get("status")) # type: ignore
development_statuses = {
	1: "Planning",
	2: "Pre-Alpha",
	3: "Alpha",
	4: "Beta",
	5: "Production/Stable",
	6: "Mature",
	7: "Inactive"
}

undefined = (None,) # Sentinel value.
setup_info = {
	"name": "sqlpyparser",
	"version": package_info.get("version"),
	"packages": find_packages(exclude=["tests", "tests.*"]),

	"author": package_info.get("author").get("name"),
	"author_email": package_info.get("author").get("email"),
	"description": package_info.get("description"),
	"keywords": " ".join(package_info.get("search_terms")) # type: ignore
		if package_info.get("search_terms") is not None else undefined,
	"url": package_info.get("site"),

	"classifiers": [
		f"Development Status :: {development_status} " +
			f"- {development_statuses.get(development_status)}",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License"
	]
}

setup(**{
	key: value for key, value in setup_info.items() if value is not undefined
})
