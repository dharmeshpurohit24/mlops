from setuptools import find_packages,setup

setup(
    name= "math-operation",
    version= "1.0",
    packages= find_packages(),
    entry_points={
        "console_scripts": [
            "math-operation=math_operation.cli:main"
        ]
    }
)