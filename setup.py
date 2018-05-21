import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vulners_scanner",
    version="0.0.1",
    author="videns",
    author_email="ibulatenko@gmail.com",
    description="vulnerability scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/videns/vulners-scanner",
    packages=setuptools.find_packages(),
    py_modules=["scanModules"],
    scripts=['vulners_scanner/linuxScanner.py', 'vulners_scanner/lazyScanner.py'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
