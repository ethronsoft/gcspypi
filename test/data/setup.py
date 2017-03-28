from setuptools import setup

setup(
    name="test_package",
    version="1.0.0",
    packages=["package"],
    install_requires=[
        "test_dep1",
        "test_dep2"
    ]
)
