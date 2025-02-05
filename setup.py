from setuptools import setup, find_packages

setup(
    name="KeepItSimpleServer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],  # No dependencies
    description="A lightweight HTTP server framework for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JMS Apps",
    url="https://github.com/jmsapps/KeepItSimpleServer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
