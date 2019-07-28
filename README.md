# easydeb

Easily create private .deb packages from a list of files. Developed and tested on debian 9.7 (stretch) with python 3.6.

## Concept

The .deb packages are created by easydeb with the following basic concept:

1. Create a temporary folder
2. Copy all files defined in the recipe to the temporary folder
3. Create the DEBIAN metadata directory with the minimum of required files
4. Build a .deb package from the temporary folder with `fakeroot` and `dpkg-deb`

**Warning**

This does not create a valid .deb package for submission to the official debian repositories. They would hate it. It simply bypasses the requirements for a real package, by adding the minimal amount of metadata required to bundle a list of files to a .deb package. Use this only for private .deb packages and if you know what you do.

## Requirements

- debian 9.7 (stretch)
- python3.6 / pip
- fakeroot (available via `apt-get install fakeroot`; https://packages.debian.org/stretch/fakeroot)

## Installation

There are two ways to install easydeb. Manually or by installing the prebundled wheel file.

**Private wheel mirror**
```console
$ pip install https://mirrors.pdrd.de/python/easydeb-1.0.0-py3-none-any.whl
```

**Manual**
```console
$ git clone https://github.com/pdrd/easydeb.git
$ cd easydeb
$ pip install -r requirements.txt
```

Optional: Add the `bin` directory to your `$PATH`.

## Usage

Run easydeb from your favorite terminal.

```console
$ easydeb --help
Usage: easydeb [OPTIONS] RECIPE BUILD_DIR OUT_DIR

Options:
  --help  Show this message and exit.
```

The `RECIPE` is a configuration file described in detail in a further section. The `BUILD_DIR` is the directory where you built the executable to distribute. The `OUT_DIR` is the directory where the final `.deb` file will be saved.

## Recipe

A recipe is simply a .json file with predefined schema. The following is the example recipe file with comments. It should be self-explanatory.

```javascript
{
    "name": "easydeb-hello", // name of package
    "version": "1.0.0", // version of package and latest changelog entry
    "arch": "amd64", // architecture the package was built for
    "section": "misc", // section of package
    "depends": "", // dependencies of package
    "description": "Hello world example from easydeb.", // description of package

    "maintainer": "Philipp Reusch", // maintainer for latest changelog entry
    "email": "philipp.reusch@skipnet.de", // email for latest changelog entry
    "changed_by": "Sun, 28 Jul 2019 17:30:00 +0000", // changed_by for latest changelog entry
 
    "files": { // specify the files to copy from the BUILD_DIR to the OUT_DIR
        "./hello.sh": "/usr/local/bin/easydeb-hello" // install BUILD_DIR/hello.sh to /usr/local/bin/easydeb-hello 
    },

    "changes": [ // changes for latest changelog entry
        "Initial custom release of easydeb-hello.",
        "Building of .deb package with easydeb."
    ],

    "shell": "/bin/bash" // specify the shell command used to run the commands
}
```

## Generated DEBIAN meta_dir

Only the minimal required files `changelog`, `compat`, `control` and `changelog` will be created based on the values specified in the recipe file.

The notation `[name]` in this chapter refers to the value defined in the recipe file.

**DEBIAN/changelog**

The following template will be used.

```
[name] ([version]) UNRELEASED; urgency=low binary-only=yes

# for change in changes:
  * [change]

 -- [name] <[email]>  [created_by]


```


**DEBIAN/compat**

The required debhelper version is **11**.

**DEBIAN/control**

The following template will be used.

```
Package: [name]
Version: [version]
Section: [section]
Priority: optional
Architecture: [arch]
Installed-Size: [size] # dynamic attribute
Maintainer: [name] <[email]>
Description: [description]
```

**DEBIAN/copyright**

This file will be empty.

## Build wheel

Run in project root:

```
$  python3 setup.py sdist bdist_wheel
```