from __future__ import annotations

import dataclasses
import os
import re
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any

PLACEHOLDER_FILES = [
    Path("src/module_name/sample_data/sample.csv"),
    Path("src/module_name/sample_data/sample.json"),
    Path("src/module_name/sample.py"),
    Path("tests/test_sample.py"),
]
PLACEHOLDER_DIR = [Path("src/module_name/sample_data")]
PYPROJECT_TARGET = Path("pyproject.toml")
README_TARGET = Path("README.md")
ORG = "Preocts"
REPO = r"python\-src\-template"
GIST = "f26cb21234ff10087c74b977705af024"


@dataclasses.dataclass
class ProjectData:
    name: str = "module_name"
    version: str = "0.0.0"
    description: str = "Module Description"
    author_email: str = "yourname@email.invalid"
    author_name: str = "[YOUR NAME]"
    org_name: str = "[ORG NAME]"
    repo_name: str = "[REPO NAME]"


def bookends(label: str) -> Callable[..., Callable[..., None]]:
    """Add start/stop print statements to functoin calls."""

    def dec_bookends(func: Callable[..., Any]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            print(f"{label}...")
            func(*args, **kwargs)
            print("Done.\n")

        return wrapper

    return dec_bookends


@bookends("Deleting placeholder files")
def delete_placeholder_files() -> None:
    """Delete placeholder files."""
    for file in PLACEHOLDER_FILES:
        if file.exists():
            os.remove(file)


@bookends("Deleting placeholder directories")
def delete_placeholder_directories() -> None:
    """Remove placeholder directories."""
    for directory in PLACEHOLDER_DIR:
        if directory.exists():
            os.rmdir(directory)


def get_input(prompt: str) -> str:
    """Extract input for ease of testing."""
    return input(prompt)


def get_project_data() -> ProjectData:
    """Query user for details on the project. This is the quiz."""
    data = ProjectData()
    for key, value in dataclasses.asdict(data).items():
        user_input = get_input(f"Enter {key} (default: {value}) : ")
        if user_input:
            setattr(data, key, user_input)
    return data


@bookends("Updating pyproject.toml values")
def replace_pyproject_values(data: ProjectData) -> None:
    """Update pyproject values."""
    pyproject = PYPROJECT_TARGET.read_text()
    for key, value in dataclasses.asdict(ProjectData()).items():
        pattern = re.compile(re.escape(value))
        pyproject = pattern.sub(getattr(data, key), pyproject)

    PYPROJECT_TARGET.write_text(pyproject)


@bookends("Updating badges in README.md")
def replace_readme_values(data: ProjectData, gist_key: str) -> None:
    """Update badge urls and placeholders in README.md"""
    readme = README_TARGET.read_text()
    default = ProjectData()

    readme = re.sub(ORG, data.org_name, readme)
    readme = re.sub(REPO, data.repo_name, readme)
    readme = re.sub(GIST, gist_key, readme)
    readme = re.sub(re.escape(default.org_name), data.org_name, readme)
    readme = re.sub(re.escape(default.repo_name), data.repo_name, readme)

    README_TARGET.write_text(readme)


if __name__ == "__main__":

    print("Eggcellent template setup:\n")

    project_data = get_project_data()
    gist_key = get_input("Enter gist key for coverage badge, leave empty to skip : ")

    replace_pyproject_values(project_data)
    replace_readme_values(project_data, gist_key or "[GIST KEY]")

    delete_placeholder_files()
    delete_placeholder_directories()
