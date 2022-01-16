import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htbuilder",
    version="0.6.0",
    author="Thiago Teixeira",
    author_email="me@thiagot.com",
    description="A purely-functional HTML builder for Python. Think JSX rather than templates.",
    license="Apache 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tvst/htbuilder",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["iteration_utilities"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
