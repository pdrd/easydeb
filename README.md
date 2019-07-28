

Create a json file with following structure:

```javascript
{
    "name": "bind-exporter", // name of package
    "version": "0.2.1", // version of package and latest changelog entry
    "arch": "amd64", // architecture the package was built for
    "section": "debug", // section of package
    "description": "Custom build from https://github.com/digitalocean/bind_exporter at 2019-07-28.", // description of package

    "maintainer": "Philipp Reusch", // maintainer for latest changelog entry
    "email": "philipp.reusch@skipnet.de", // email for latest changelog entry
    "changed_by": "Sat, 27 Jul 2019 23:19:22 +0000", // changed_by for latest changelog entry
 
    "files": { // specify the files to copy from the BUILD_DIR to the OUT_DIR
        "./bind_exporter": "/usr/local/bin/bind_exporter"
    },

    "changes": [ // changes for latest changelog entry
        "Initial custom release of bind-exporter.",
        "Building of .deb package with easydeb."
    ],

    "shell": "/bin/bash" // specify the shell command used to run the commands
}
```


development and testing with python 3.6

pip has to be available

install requirements from file:

```bash
pip install -r requirements.txt
```


control file will be created:

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

compat is version 11

copyright is empty

changelog will contain one entry

```
[name] ([version]) UNRELEASED; urgency=low binary-only=yes

# for change in changes:
  * [change]

 -- [name] <[email]>  [created_by]


```