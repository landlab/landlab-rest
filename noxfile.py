import os
import pathlib
import shutil

import nox

PROJECT = "landlab_rest"
ROOT = pathlib.Path(__file__).parent


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-e", ".[dev]")

    args = session.posargs or ["-n", "auto", "--cov", PROJECT, "-vvv"]
    if "CI" in os.environ:
        args.append("--cov-report=xml:$(pwd)/coverage.xml")
    session.run("pytest", *args)
    # "--fail-under=100",


@nox.session(name="test-cli")
def test_cli(session: nox.Session) -> None:
    """Test the command line interface."""
    session.install(".")
    session.run("start-sketchbook", "--help")
    session.run("start-sketchbook", "--version")


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")

    args = list(session.posargs)
    args.append("--all-files")
    if "CI" in os.environ:
        args.append("--show-diff-on-failure")

    session.run("pre-commit", "run", *args)

    # towncrier(session)


@nox.session
def towncrier(session: nox.Session) -> None:
    """Check that there is a news fragment."""
    session.install("towncrier")
    session.run("towncrier", "check", "--compare-with", "origin/master")


@nox.session(name="build-docs", reuse_venv=True)
def build_docs(session: nox.Session) -> None:
    """Build the docs."""
    session.install(".[docs]")

    clean_docs(session)
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        str(ROOT / "docs/source"),
        str(ROOT / "docs/build/html"),
    )


@nox.session(name="live-docs", reuse_venv=True)
def live_docs(session: nox.Session) -> None:
    session.install(".[docs]")
    session.run(
        "sphinx-autobuild",
        "-b",
        "html",
        "docs/source",
        "docs/build/html",
        "--open-browser",
    )


@nox.session(name="build-requirements", reuse_venv=True)
def build_requirements(session: nox.Session) -> None:
    """Create requirements files from pyproject.toml."""
    session.install("tomli")

    with open("requirements.txt", "w") as fp:
        session.run("python", "requirements.py", stdout=fp)

    for extra in ["dev", "docs"]:
        with open(f"requirements-{extra}.txt", "w") as fp:
            session.run("python", "requirements.py", extra, stdout=fp)


@nox.session
def build(session: nox.Session) -> None:
    """Build sdist and wheel dists."""
    session.install("pip")
    session.install("build")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run("python", "-m", "build", "--outdir", "./wheelhouse")


@nox.session
def release(session):
    """Tag, build and publish a new release to PyPI."""
    session.install("zest.releaser[recommended]")
    session.install("zestreleaser.towncrier")
    session.run("fullrelease")


@nox.session
def publish_testpypi(session):
    """Publish wheelhouse/* to TestPyPI."""
    session.run("twine", "check", "wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "wheelhouse/*.tar.gz",
    )


@nox.session
def publish_pypi(session):
    """Publish wheelhouse/* to PyPI."""
    session.run("twine", "check", "wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "wheelhouse/*.tar.gz",
    )


@nox.session(python=False)
def clean(session):
    """Remove all .venv's, build files and caches in the directory."""
    for folder in _args_to_folders(session.posargs):
        with session.chdir(folder):

            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("wheelhouse", ignore_errors=True)
            shutil.rmtree(f"{PROJECT}.egg-info", ignore_errors=True)
            shutil.rmtree(".pytest_cache", ignore_errors=True)
            shutil.rmtree(".venv", ignore_errors=True)

            for pattern in ["*.py[co]", "__pycache__"]:
                _clean_rglob(pattern)


@nox.session(python=False, name="clean-checkpoints")
def clean_checkpoints(session):
    """Remove jupyter notebook checkpoint files."""
    for folder in _args_to_folders(session.posargs):
        with session.chdir(folder):
            _clean_rglob("*-checkpoint.ipynb")
            _clean_rglob(".ipynb_checkpoints")


@nox.session(python=False, name="clean-docs")
def clean_docs(session: nox.Session) -> None:
    """Clean up the docs folder."""
    session.chdir(ROOT / "docs")
    if os.path.exists("build"):
        shutil.rmtree("build")


@nox.session(python=False, name="clean-ext")
def clean_ext(session: nox.Session) -> None:
    """Clean shared libraries for extension modules."""
    for folder in _args_to_folders(session.posargs):
        with session.chdir(folder):
            _clean_rglob("*.so")


@nox.session(python=False)
def nuke(session):
    """Run all clean sessions."""
    clean_checkpoints(session)
    clean_docs(session)
    clean(session)
    clean_ext(session)


def _args_to_folders(args):
    return [ROOT] if not args else [pathlib.Path(f) for f in args]


def _clean_rglob(pattern):
    nox_dir = pathlib.Path(".nox")

    for p in pathlib.Path(".").rglob(pattern):
        if nox_dir in p.parents:
            continue
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()
