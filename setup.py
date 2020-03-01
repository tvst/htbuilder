import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htbuild",
    version="0.0.1",
    author="Thiago Teixeira",
    author_email="me@thiagot.com",
    description="Tiny HTML string builder for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tvst/htbuild",
    packages=setuptools.find_packages(),
    install_requires=["iteration_utilities"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
