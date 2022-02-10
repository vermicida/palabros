#!/usr/bin/env python3

import json
import re
import subprocess
import sys
from typing import List, Optional, Tuple
from uuid import uuid4

from requests import get
from semver import VersionInfo

pattern = re.compile("^(\d+)\.(\d+)\.(\d+)[\.\-]dev\.?(\d+)$")

repositories = {
    "pypi": "https://upload.pypi.org/legacy/",
    "testpypi": "https://test.pypi.org/legacy/",
}


def exit(message: Optional[str] = None, status: int = 0) -> None:

    """
    Exit the script with the given message and status.

    Args:
        message: A message to display in the console.
        status: The result of the script execution.
    """

    if message is not None:
        print(f"\n{message}\n")

    sys.exit(status)


def get_package_releases(package: str) -> List[VersionInfo]:

    """
    Retrieve the developmental releases of a given package from TestPyPI.

    Args:
        package: The package name.

    Returns:
        A list with the developmental releases retrieved.
    """

    res = get(
        f"https://testpypi.python.org/pypi/{package}/json",
        params={"q": str(uuid4()).split("-")[-1]},
    )

    # Unexisting package.
    if res.status_code == 404:
        return []

    # Wrong server response.
    if res.status_code != 200:
        exit(message=f"Wrong TestPyPI server response {res.status_code}", status=1)

    # Server response not deserializable.
    try:
        data = res.json()
    except json.JSONDecodeError:
        exit(message="TestPyPI server response could not be deserialized", status=2)

    # Package with no releases yet.
    if "releases" not in data or not bool(data["releases"]):
        return []

    releases = []
    for r in data["releases"].keys():
        m = pattern.search(r)
        if m is not None:
            v = f"{m.group(1)}.{m.group(2)}.{m.group(3)}-dev.{m.group(4)}"
            releases.append(VersionInfo.parse(v))

    return releases


def get_package_next_release(package: str, version: str) -> str:

    """
    Generate the next valid developmental release for the given package and version.

    Args:
        package: The package name.
        version: The package version.

    Returns:
        The next valid developmental release.
    """

    version = VersionInfo.parse(version)

    releases = [
        release
        for release in get_package_releases(package)
        if release.major == version.major
        and release.minor == version.minor
        and release.patch == version.patch
        and release.prerelease.startswith("dev")
    ]

    if len(releases) > 0:
        return str(sorted(releases)[-1].bump_prerelease(token="dev"))

    return str(version.bump_prerelease(token="dev"))


def execute(command: str, cwd: Optional[str] = None) -> str:

    """
    Run the given command.

    Args:
        command: The command to execute.
        cwd: The working directory in which the command must be run.

    Returns:
        The result of the command execution.
    """

    options = {
        "check": True,
        "shell": True,
        "stdout": subprocess.PIPE,
        "universal_newlines": True,
    }

    if cwd is not None:
        options["cwd"] = cwd

    try:
        response = subprocess.run(command, **options).stdout
    except subprocess.CalledProcessError as err:
        exit(message=f"Command '{err.cmd}' failed with status {err.returncode}", status=3)

    return response


def get_package_metadata() -> Tuple[str, str]:

    """
    Get the current package metadata.

    Returns:
        A tuple with the package name and version.
    """

    response = execute("poetry version")
    return tuple([m.strip() for m in response.split(" ")])


def publish(repository: str, token: str) -> None:

    """
    Build and publish a new package release.

    Args:
        repository: The repository in which the package must be published.
        token: A valid token to sign the requests to the repository server.
    """

    if repository not in repositories:
        repository = "testpypi"

    if repository == "testpypi":
        package, version = get_package_metadata()
        release = get_package_next_release(package, version)
        execute(f"poetry version {release}")

    execute(f"poetry config pypi-token.{repository} {token}")
    execute(f"poetry config repositories.{repository} {repositories[repository]}")
    execute("poetry build")
    execute(f"poetry publish --repository {repository}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(message="Usage: ./entrypoint.sh [repository] [token]", status=4)
    publish(sys.argv[1], sys.argv[2])
    exit(status=0)
