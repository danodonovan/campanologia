from setuptools import setup, find_packages

setup(
    name='campanologia',
    packages=find_packages(
        include=["bells", "bells.*", "methods", "methods.*"],
        exclude=["*.tests", "*.tests.*"]
    ),
)
