from setuptools import setup, find_packages

setup(
    name="time-checker",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "time-check=time_checker.cli:main"
        ]
    }
)
