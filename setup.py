import setuptools
from pathlib import Path
import re


def fetch_version() -> str:

    content = (Path(__file__).parent / "tgbotscenario" / "__init__.py").read_text(encoding="UTF-8")
    try:
        version_string = re.findall(r'__version__ = \"\d+\.\d+\.\d+\"', content)[0]
        version = version_string.rsplit(" ", 1)[-1].replace('"', '')
    except IndexError:
        raise RuntimeError("version not found!")

    return version


setuptools.setup(
    name="tgbotscenario",
    version=fetch_version(),
    packages=setuptools.find_packages(exclude=("tests",)),
    url="https://github.com/Abstract-X/tgbotscenario",
    license="MIT",
    author="Abstract-X",
    author_email="abstract-x-mail@protonmail.com",
    description="Scene-based FSM implementation for Telegram bots.",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    python_requires='>=3.7'
)
