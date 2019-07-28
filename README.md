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

### Private wheel mirror

```console
$ pip install https://mirrors.pdrd.de/python/easydeb-1.0.0-py3-none-any.whl
```

### Manual

```console
$ git clone https://github.com/pdrd/easydeb.git
$ cd easydeb
$ pip install -r requirements.txt
```

Optional: Add the `bin` directory to your `$PATH`.

#### Build wheel

Run in project root:

```
$  python3 setup.py sdist bdist_wheel
```

## Usage

Run easydeb from your favorite terminal.

```console
$ easydeb --help
Usage: easydeb [OPTIONS] RECIPE BUILD_DIR OUT_DIR

Options:
  --help  Show this message and exit.
```

The `RECIPE` is the path to a configuration file described in the `Example` and `Recipe` sections. The `BUILD_DIR` is the directory where you built the executable to distribute. The `OUT_DIR` is the directory where the final `.deb` file will be saved.

## Example

Take a look at the [example](example) in the repository. You can access it via the browser or clone the repository.

**Files**
- example/build_deb.sh - build the .deb file
- example/hello.json - easydeb recipe file
- example/hello.sh - executable to bundle

The example bundles a simple shell file [hello.sh](example/hello.sh):

```bash
#!/bin/bash

if [ -z "$1" ]; then
    echo "You don't wanna tell me you're name?"
else
    echo "Hello $1!"
fi
```

It prints `Hello [arg1]!` to the screen, if the first argument exists, otherwise it prints another message.

To create the bundled .deb file, simple execute the shell file [build_deb.sh](example/build_deb.sh). It sets the environment variables and calls easydeb:

```console
$ RECIPE="./hello.json" # path to easydeb recipe file
$ BUILD_DIR="./" # path to binary files
$ OUT_DIR="./" # the .deb file will be placed here
$ easydeb "$RECIPE" "$BUILD_DIR" "$OUT_DIR" 
dpkg-deb: building package 'easydeb-hello' in '/opt/easydeb/example/easydeb-hello_1.0.0_amd64.deb'.
Generated package /opt/easydeb/example/easydeb-hello_1.0.0_amd64.deb.
```

The used recipe file [hello.json](example/hello.json) has the following content:

```javascript
{
    "name": "easydeb-hello", // name of package
    "version": "1.0.0", // version of package and latest changelog entry
    "arch": "amd64", // architecture the package was built for
    "section": "misc", // section of package
    "depends": "", // dependencies of package
    "description": "Hello world example from easydeb.", // description of package

    "maintainer": "John Doe", // maintainer for latest changelog entry
    "email": "john@example.com", // email for latest changelog entry
    "changed_by": "Mon, 04 May 2019 00:11:22 +0000", // changed_by for latest changelog entry
 
    "files": { // specify the files to copy from the BUILD_DIR to the OUT_DIR
        "./hello.sh": "/usr/local/bin/easydeb-hello" // installs BUILD_DIR/hello.sh to /usr/local/bin/easydeb-hello 
    },

    "changes": [ // changes for latest changelog entry
        "Initial custom release of easydeb-hello.",
        "Building of .deb package with easydeb."
    ],

    "shell": "/bin/bash" // specify the shell command used to run the commands
}
```

After building the `easydeb-hello_1.0.0_amd64.deb`, it can be installed via:

```console
$ dpkg -i easydeb-hello_1.0.0_amd64.deb 
Selecting previously unselected package easydeb-hello.
(Reading database ... 83093 files and directories currently installed.)
Preparing to unpack easydeb-hello_1.0.0_amd64.deb ...
Unpacking easydeb-hello (1.0.0) ...
Setting up easydeb-hello (1.0.0) ...
```

From now on the shell script [hello.sh](example/hello.sh) is installed under `/usr/local/bin/easydeb-hello` and if `/usr/local/bin` is available on `$PATH` it can be called like this:

```console
$ easydeb-hello "world"
Hello world!
```

The package information can be queried via dpkg:

```console
$ dpkg -s easydeb-hello
Package: easydeb-hello
Status: install ok installed
Priority: optional
Section: misc
Installed-Size: 110
Maintainer: John Doe <john@example.com>
Architecture: amd64
Version: 1.0.0
Description: Hello world example from easydeb.
```

The package can be removed via it's name:

```console
$ dpkg -r easydeb-hello
```

## Recipe

A recipe is simply a .json file with predefined schema. The schema follows the [json-schema.org](https://json-schema.org/) drafts and is defined in [src/easydeb](src/easydeb). Because of the pretty self-explanatory structure, take a look at the `Example` section with the example recipe file [hello.json](example/hello.json).

Apart from that the `Generated DEBIAN meta_dir` section contains information about where the variables from the recipe file are used.

## Metadata in /DEBIAN

Packaging for debian is a very complicated task, which is for some extents documented on[wiki.debian.org/Packaging](https://wiki.debian.org/Packaging). The policy for packages are very strict and this is good. It makes debian one of the most-stable distributions out there.

Easydeb bypasses most of the policies and creates only the files, which are required at minimum to package a .deb file with `dpkg-deb`. To avoid any problems with this, easydeb uses the following defaults:

- **DEBIAN/changelog**: The `distributions` value is `UNRELEASED`, which disables the upload to a public repository. Reference: [debian.org maint-guide](https://www.debian.org/doc/manuals/maint-guide/dreq.en.html)
- **DEBIAN/control**: The `Priority` is `optional`, because "Packages with a priority of optional may conflict with each other." Reference: [debian.org policy - priorities](https://www.debian.org/doc/debian-policy/ch-archive.html#s-priorities)

The following subsections describe, how the corresponding files are created. The notation `[name]` in this chapter refers to the value defined in the recipe file.

#### DEBIAN/changelog

The following template will be used.

```
[name] ([version]) UNRELEASED; urgency=low binary-only=yes

# for change in [changes]:
  * [change]

 -- [name] <[email]>  [created_by]


```


#### DEBIAN/compat

The required debhelper version and the file content is **11**.

#### DEBIAN/control

The following template will be used.

```
Package: [name]
Version: [version]
Depends: [depends]
Section: [section]
Priority: optional
Architecture: [arch]
Installed-Size: [size] # dynamic attribute
Maintainer: [name] <[email]>
Description: [description]
```

#### DEBIAN/copyright

This file will be empty.

## License

The MIT License - see [LICENSE](LICENSE) file.
