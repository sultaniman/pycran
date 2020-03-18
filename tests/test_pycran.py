from pycran import from_cran_format, from_packages_list, to_cran_format


def test_package_list_parser():
    data = """
    Package: ABACUS
    Version: 1.0.0
    Depends: R (>= 3.1.0)
    Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
    Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
    License: GPL-3
    MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
    NeedsCompilation: no

    Package: abbyyR
    Version: 0.5.5
    Depends: R (>= 3.2.0)
    Imports: httr, XML, curl, readr, plyr, progress
    Suggests: testthat, rmarkdown, knitr (>= 1.11), lintr
    License: MIT + file LICENSE
    MD5sum: e048a3bca6ea32126e6c367415c0bfaf
    NeedsCompilation: no
    """
    packages = [p for p in from_packages_list(data)]
    assert len(packages) == 2
    assert packages[0] == {
        "Package": "ABACUS",
        "Version": "1.0.0",
        "Depends": "R (>= 3.1.0)",
        "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
        "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
        "License": "GPL-3",
        "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
        "NeedsCompilation": "no"
    }

    assert [p for p in from_packages_list("")] == []

    data = """Package: abc
    Version: 2.1
    Depends: R (>= 2.10), abc.data, nnet, quantreg, MASS, locfit
    License: GPL (>= 3)
    MD5sum: c9fffe4334c178917f762735aba59653
    NeedsCompilation: no
    Package: abc.data
    Version: 1.0
    Depends: R (>= 2.10)
    License: GPL (>= 3)
    MD5sum: 799079dbbdd0cfc9d9c61c3e35241806
    NeedsCompilation: no"""
    assert len([p for p in from_packages_list(data)]) == 2

    data = """
    Package: ABACUS
    Version: 1.0.0
    Depends: R (>= 3.1.0)
    Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
    Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
    License: GPL-3
    MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
    NeedsCompilation: no
    Package: abbyyR
    Version: 0.5.5
    Depends: R (>= 3.2.0)
    Imports: httr, XML, curl, readr, plyr, progress
    Suggests: testthat, rmarkdown, knitr (>= 1.11), lintr
    License: MIT + file LICENSE
    MD5sum: e048a3bca6ea32126e6c367415c0bfaf
    NeedsCompilation: no
    """
    assert len([p for p in from_packages_list(data)]) == 2

    data = b"""
    Package: ABACUS
    Version: 1.0.0
    Depends: R (>= 3.1.0)
    Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
    Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
    License: GPL-3
    MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
    NeedsCompilation: no
    Package: abbyyR
    Version: 0.5.5
    Depends: R (>= 3.2.0)
    Imports: httr, XML, curl, readr, plyr, progress
    Suggests: testthat, rmarkdown, knitr (>= 1.11), lintr
    License: MIT + file LICENSE
    MD5sum: e048a3bca6ea32126e6c367415c0bfaf
    NeedsCompilation: no
    """
    assert len([p for p in from_packages_list(data)]) == 2


def test_to_cran_format():
    metadata = """
    Package: ABACUS
    Version: 1.0.0
    Depends: R (>= 3.1.0)
    Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
    Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
    License: GPL-3
    MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
    NeedsCompilation: no
    """
    result = to_cran_format({
        "Package": "ABACUS",
        "Version": "1.0.0",
        "Depends": "R (>= 3.1.0)",
        "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
        "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
        "License": "GPL-3",
        "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
        "NeedsCompilation": "no"
    })

    def clean(data):
        return "\n".join([line.strip() for line in data.split("\n")]).strip()

    # we want to assert result and expected result without
    # any leading or trailing spaces thus cutting them off.
    assert clean(metadata) == clean(result)


def test_from_cran_format():
    deb_data = """
    Package: ABACUS
    Version: 1.0.0
    Depends: R (>= 3.1.0)
    Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),
    Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)
    License: GPL-3
    MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd
    NeedsCompilation: no
    """
    expected = {
        "Package": "ABACUS",
        "Version": "1.0.0",
        "Depends": "R (>= 3.1.0)",
        "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
        "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
        "License": "GPL-3",
        "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
        "NeedsCompilation": "no"
    }

    assert from_cran_format(deb_data) == expected
