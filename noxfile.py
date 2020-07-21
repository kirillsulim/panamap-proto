import nox


LINE_LENGTH = 120

STYLE_TARGETS = [
    "panamap_proto",
    "tests/test_proto_mapping.py",
    "noxfile.py",
    "setup.py",
]

FLAKE8_IGNORE = [
    "E203",
    "E231",
    "W503",
]


@nox.session
def unit_tests(session):
    session.install(".")
    session.install("pytest")
    session.install("coverage")
    session.run("coverage", "run", "--source", "panamap_proto", "-m", "pytest", "tests")


@nox.session
def style(session):
    session.install("flake8", "black", "isort")

    session.run("black", "--version")
    session.run("black", "--check", "--target-version", "py38", "--line-length", f"{LINE_LENGTH}", *STYLE_TARGETS)

    session.run("flake8", "--version")
    session.run(
        "flake8",
        "--max-line-length",
        f"{LINE_LENGTH}",
        "--extend-ignore",
        ",".join(FLAKE8_IGNORE),
        "--show-source",
        *STYLE_TARGETS,
    )
