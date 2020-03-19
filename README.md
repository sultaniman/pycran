[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycran?label=Python)](https://pypi.org/project/pycran/)
[![Build Status](https://travis-ci.com/imanhodjaev/pycran.svg?branch=master)](https://travis-ci.com/imanhodjaev/pycran)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef60de33a4dcebb61689/maintainability)](https://codeclimate.com/github/imanhodjaev/pycran/maintainability)
[![codecov](https://codecov.io/gh/imanhodjaev/pycran/branch/master/graph/badge.svg)](https://codecov.io/gh/imanhodjaev/pycran)
[![PyPI - License](https://img.shields.io/pypi/l/pycran?color=ff69b4&label=License)](https://opensource.org/licenses/Apache-2.0)

<p align="center">
  <h1 align="center">PyCran</h1>
</p>

## Overview 👀
Yet another metadata parser for R source packages and R metadata information

```ini
Package: ABACUS
Version: 1.0.0
Depends: R (>= 3.1.0)
Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
License: GPL-3
MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
NeedsCompilation: no
```

For more see: https://cran.r-project.org/src/contrib/PACKAGES

PyCran lets us parse raw metadata and get it as dictionary, you can:

1. Encode metadata dictionary to raw format,
2. Decode raw metadata and receive it as dictionary,
3. Load from tar archive with R library sources.


## Installation 💾

```sh
$ pip install pycran
```

## Usage 🚀

### Decode
```python
import pycran

raw_metadata = """
Package: ABACUS
Version: 1.0.0
Depends: R (>= 3.1.0)
Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
License: GPL-3
MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
NeedsCompilation: no
"""

assert pycran.decode(raw_metadata) == {
    "Package": "ABACUS",
    "Version": "1.0.0",
    "Depends": "R (>= 3.1.0)",
    "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
    "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
    "License": "GPL-3",
    "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
    "NeedsCompilation": "no",
}
```

### Encode

```python
import pycran

metadata = {
    "Package": "ABACUS",
    "Version": "1.0.0",
    "Depends": "R (>= 3.1.0)",
    "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
    "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
    "License": "GPL-3",
    "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
    "NeedsCompilation": "no",
}

expected = """
Package: ABACUS
Version: 1.0.0
Depends: R (>= 3.1.0)
Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
License: GPL-3
MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
NeedsCompilation: no
"""

assert pycran.encode(metadata) == expected
```

### Load from R source archive

```python
import pycran

# you can pass path to archive
pycran.from_file("PATH/TO/PACKAGE/ABACUS_1.0.0.tar.gz")

# or you can pass tarfile object
import tarfile

pycran.from_file(tarfile.open("PATH/TO/PACKAGE/ABACUS_1.0.0.tar.gz"))
```

### Parse raw metadata

In cases when you need to parse metadata for multiple
packages you can pass the data to `pycran.parse` function

```python
import pycran

# somehow you download the contents of https://cran.r-project.org/src/contrib/PACKAGES
package_list = requests.get(https://cran.r-project.org/src/contrib/PACKAGES).text()

# And parse it as a result you will get a generator which you can iterate
pycran.parse(package_list)
```

<h2 align="center">Enjoy!&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h2>
<p align="center">
        ✨ 🍰 ✨&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</p>
