import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easydeb",
    version="1.0.0",
    author="Philipp Reusch",
    author_email="philipp.reusch@skipnet.de",
    description="Create private .deb packages from binary files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pdrd/easydeb",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    install_requires=['Click==7.*','jsonschema==3.*'],
    scripts=['src/easydeb'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)