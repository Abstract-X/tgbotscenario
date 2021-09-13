import setuptools


setuptools.setup(
    name="tgbotscenario",
    version="0.4.1",
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
