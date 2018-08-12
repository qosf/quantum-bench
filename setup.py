import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quenchmark",
    version="0.0.1",
    author="Tomas Babej, Mark Fingerhuth",
    author_email="research@tbabej.com, markfingerhuth@protonmail.com",
    description="Benchmark suite for open-source quantum software projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
