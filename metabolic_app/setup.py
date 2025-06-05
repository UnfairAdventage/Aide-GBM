from setuptools import setup, find_packages

setup(
    name="metabolic_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "PyQt5",
    ],
) 