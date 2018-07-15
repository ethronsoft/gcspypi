from setuptools import setup

setup(
    name="other_package",
    version="1.0.0",
    packages=["package"],
    install_requires=[
        "test_dep1",
        "test_package==1.0.0"
    ]
)
