"""Nox sessions."""
from pathlib import Path
import re
import tempfile
from typing import Any

import nox  # type: ignore
from nox.sessions import Session  # type: ignore

# Name of the package.
PACKAGE = "binance_api_fetcher"

# Sessions to run by running nox.
nox.options.sessions = "lint", "mypy", "safety", "test"

# Locations to run commands against.
LOCATIONS = "src", "tests", "./noxfile.py", "docs/conf.py"

# Path to the folder containing the nox file.
HERE = Path(__file__).parent

# Regular expression for Python (semantic) version.
PYTHON_VERSION_REX = re.compile(r"(\d\.\d+)\.\d")


class Version:
    """Represents python version.

    Args:
        major: Major version.
        minor: Minor version.
    """

    def __init__(self, major: int, minor: int) -> None:
        self.major = major
        self.minor = minor

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.major}, {self.minor})"

    def __lt__(self, other: Any) -> bool:
        if not type(self) is type(other):
            return False
        if self.major < other.major:
            return True
        if self.major == other.major and self.minor < other.minor:
            return True
        return False

    def __eq__(self, other: Any) -> bool:
        if not type(self) is type(other):
            return False
        return self.major == other.major and self.minor == other.minor

    @classmethod
    def from_string(cls, version: str) -> "Version":
        """Initialize class from string.

        Args:
            version: String in the format '{major}.{minor}'

        Returns:
            str: Version object.
        """
        major, minor = version.split(".")
        return cls(major=int(major), minor=int(minor))


# Python versions used by the project (pyenv).
_pyenv_versions = (HERE / ".python-version").read_text().strip().split("\n")
python_versions = []
for version in _pyenv_versions:
    search = PYTHON_VERSION_REX.search(version)
    if search:
        python_versions.append(search.group(1))

# Version Python used for main development (first entry in .python-version file).
dev_python = python_versions[0]

# Python versions used by the project sorted.
python_versions = list(
    map(str, sorted([Version.from_string(v) for v in python_versions]))
)


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Args:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            "--without-hashes",
            external=True,
        )
        session.install(f"--requirement={requirements.name}", *args, **kwargs)


@nox.session(python=dev_python)
def black(session: Session) -> None:
    """Run black code formatter.

    Args:
        session: The Session object.
    """
    args = session.posargs or LOCATIONS
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=python_versions)
def lint(session: Session) -> None:
    """Lint using flake8.

    Args:
        session: The Session object.
    """
    args = session.posargs or LOCATIONS
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Args:
        session: The Session object.
    """
    args = session.posargs or LOCATIONS
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=dev_python)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages.

    Args:
        session: The Session object.
    """
    install_with_constraints(session, "safety")
    session.run("safety", "check", "--full-report")


@nox.session(name="test", python=python_versions)
def pytest(session: Session) -> None:
    """Run the test suite.

    Args:
        session: The Session object.
    """
    args = session.posargs or ["--cov"]
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "typeguard"
    )
    session.install(".")
    session.run(
        "pytest",
        f"--typeguard-packages={PACKAGE}",
        *args,
    )


@nox.session(name="test-unit", python=python_versions)
def pytest_unit(session: Session) -> None:
    """Run unit tests.

    Args:
        session: The Session object.
    """
    args = session.posargs or ["--cov"]
    session.install(".")
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "typeguard"
    )
    session.run(
        "pytest",
        "-m",
        "unit",
        f"--typeguard-packages={PACKAGE}",
        *args,
    )


@nox.session(name="test-integration", python=python_versions)
def pytest_integration(session: Session) -> None:
    """Run integration tests.

    Args:
        session: The Session object.
    """
    args = session.posargs or ["--cov"]
    session.install(".")
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "typeguard"
    )
    session.run(
        "pytest",
        "-m",
        "integration",
        f"--typeguard-packages={PACKAGE}",
        *args,
    )


@nox.session(name="test-e2e", python=python_versions)
def pytest_e2e(session: Session) -> None:
    """Run e2e tests.

    Args:
        session: The Session object.
    """
    args = session.posargs or ["--cov"]
    session.install(".")
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "typeguard"
    )
    session.run(
        "pytest",
        "-m",
        "e2e",
        f"--typeguard-packages={PACKAGE}",
        *args,
    )


@nox.session(python=dev_python)
def docs(session: Session) -> None:
    """Build the documentation.

    Args:
        session: The Session object.
    """
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=dev_python)
def cover(session: Session) -> None:
    """Run the final coverage report.

    Args:
        session: The Session object.
    """
    session.install("coverage[toml]")
    session.run("coverage", "html")
