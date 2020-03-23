import tarfile
from os import path
from zipfile import ZipFile

import pytest

import pycran
from pycran.errors import DescriptionNotFound, NotTarFile

data_path = path.join(path.dirname(__file__), "data")


def test_parse_works_with_normal_data():
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
    packages = list(pycran.parse(data))
    assert len(packages) == 2
    assert packages[0] == {
        "Package": "ABACUS",
        "Version": "1.0.0",
        "Depends": "R (>= 3.1.0)",
        "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
        "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
        "License": "GPL-3",
        "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
        "NeedsCompilation": "no",
    }


def test_parse_works_with_empty_data():
    assert list(pycran.parse("")) == []


def test_parse_works_on_non_separated_data():
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
    result = list(pycran.parse(data))
    assert len(result) == 2
    assert result == [
        {
            "Package": "abc",
            "Version": "2.1",
            "Depends": "R (>= 2.10), abc.data, nnet, quantreg, MASS, locfit",
            "License": "GPL (>= 3)",
            "MD5sum": "c9fffe4334c178917f762735aba59653",
            "NeedsCompilation": "no",
        },
        {
            "Package": "abc.data",
            "Version": "1.0",
            "Depends": "R (>= 2.10)",
            "License": "GPL (>= 3)",
            "MD5sum": "799079dbbdd0cfc9d9c61c3e35241806",
            "NeedsCompilation": "no",
        },
    ]

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

    assert len(list(pycran.parse(data))) == 2


def test_parse_works_on_mixed_data():
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
    result = list(pycran.parse(data))
    assert len(result) == 3
    assert result == [
        {
            "Package": "abc",
            "Version": "2.1",
            "Depends": "R (>= 2.10), abc.data, nnet, quantreg, MASS, locfit",
            "License": "GPL (>= 3)",
            "MD5sum": "c9fffe4334c178917f762735aba59653",
            "NeedsCompilation": "no",
        },
        {
            "Package": "abc.data",
            "Version": "1.0",
            "Depends": "R (>= 2.10)",
            "License": "GPL (>= 3)",
            "MD5sum": "799079dbbdd0cfc9d9c61c3e35241806",
            "NeedsCompilation": "no",
        },
        {
            "Package": "abbyyR",
            "Version": "0.5.5",
            "Depends": "R (>= 3.2.0)",
            "Imports": "httr, XML, curl, readr, plyr, progress",
            "Suggests": "testthat, rmarkdown, knitr (>= 1.11), lintr",
            "License": "MIT + file LICENSE",
            "MD5sum": "e048a3bca6ea32126e6c367415c0bfaf",
            "NeedsCompilation": "no",
        },
    ]


def test_parse_properly_parses_non_field_lines():
    data = b"""
    Package: abbyyR
    Title: Access to Abbyy Optical Character Recognition (OCR) API
    Version: 0.5.5
    Authors@R: person("Gaurav", "Sood", email = "gsood07@gmail.com", role = c("aut", "cre"))
    Maintainer: Gaurav Sood <gsood07@gmail.com>
    Description: Get text from images of text using Abbyy Cloud Optical Character
        Recognition (OCR) API. Easily OCR images, barcodes, forms, documents with
        machine readable zones, e.g. passports. Get the results in a variety of formats
        including plain text and XML. To learn more about the Abbyy OCR API, see 
        <http://ocrsdk.com/>.
    URL: http://github.com/soodoku/abbyyR
    BugReports: http://github.com/soodoku/abbyyR/issues
    Depends: R (>= 3.2.0)
    License: MIT + file LICENSE
    LazyData: true
    VignetteBuilder: knitr
    Imports: httr, XML, curl, readr, plyr, progress
    Suggests: testthat, rmarkdown, knitr (>= 1.11), lintr
    RoxygenNote: 6.1.1
    NeedsCompilation: no
    Packaged: 2019-06-25 01:30:58 UTC; soodoku
    Author: Gaurav Sood [aut, cre]
    Repository: CRAN
    Date/Publication: 2019-06-25 04:30:04 UTC
    """
    [package] = list(pycran.parse(data))
    assert "<http" not in package
    assert "<http://ocrsdk.com/>" in package["Description"]


def test_parse_works_with_binary_data():
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
    assert len(list(pycran.parse(data))) == 2


def test_parse_can_parse_all_entries_from_cran_registry():
    # Test on real package metadata from https://cran.r-project.org/src/contrib/PACKAGES
    with ZipFile(path.join(data_path, "PACKAGES.txt.zip")) as archive:
        with archive.open("PACKAGES.txt") as fp:
            assert len(list(pycran.parse(fp.read()))) == 15398


def test_parse_can_parse_mixed_entries_from_cran_registry():
    with open(path.join(data_path, "PACKAGES_MIX.txt")) as fp:
        assert list(pycran.parse(fp.read())) == [
            {
                "Package": "A3",
                "Version": "1.0.0",
                "Depends": "R (>= 2.15.0), xtable, pbapply",
                "Suggests": "randomForest, e1071",
                "License": "GPL (>= 2)",
                "MD5sum": "027ebdd8affce8f0effaecfcd5f5ade2",
                "NeedsCompilation": "no",
            },
            {
                "Package": "A8",
                "Version": "1.0.0",
                "Depends": "R (>= 2.15.0), xtable, pbapply",
                "Suggests": "randomForest, e1071",
                "License": "GPL (>= 2)",
                "MD5sum": "027ebdd8affce8f0effaecfcd5f5ade2",
                "NeedsCompilation": "no",
            },
            {
                "Package": "aaSEA",
                "Version": "1.1.0",
                "Depends": "R(>= 3.4.0)",
                "Imports": "DT(>= 0.4), networkD3(>= 0.4), shiny(>= 1.0.5), shinydashboard(>= 0.7.0), magrittr(>= 1.5), Bios2cor(>= 2.0), seqinr(>= 3.4-5), plotly(>= 4.7.1), Hmisc(>= 4.1-1)",
                "Suggests": "knitr, rmarkdown",
                "License": "GPL-3",
                "MD5sum": "0f9aaefc1f1cf18b6167f85dab3180d8",
                "NeedsCompilation": "no",
            },
        ]


def test_encode():
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
    result = pycran.encode(
        {
            "Package": "ABACUS",
            "Version": "1.0.0",
            "Depends": "R (>= 3.1.0)",
            "Imports": "ggplot2 (>= 3.1.0), shiny (>= 1.3.1),",
            "Suggests": "rmarkdown (>= 1.13), knitr (>= 1.22)",
            "License": "GPL-3",
            "MD5sum": "50c54c4da09307cb95a70aaaa54b9fbd",
            "NeedsCompilation": "no",
        }
    )

    def clean(data):
        return "\n".join([line.strip() for line in data.split("\n")]).strip()

    # we want to assert result and expected result without
    # any leading or trailing spaces thus cutting them off.
    assert clean(metadata) == clean(result)


def test_decode_works():
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
        "NeedsCompilation": "no",
    }

    assert pycran.decode(deb_data) == expected


def test_decode_returns_none_if_empty_string_given():
    assert pycran.decode("") is None


def test_from_file_path_works():
    assert pycran.from_file(path.join(data_path, "A3_1.0.0.tar.gz")) == {
        "Package": "A3",
        "Type": "Package",
        "Title": "Accurate, Adaptable, and Accessible Error Metrics for Predictive Models",
        "Version": "1.0.0",
        "Date": "2015-08-15",
        "Author": "Scott Fortmann-Roe",
        "Maintainer": "Scott Fortmann-Roe <scottfr@berkeley.edu>",
        "Description": "Supplies tools for tabulating and analyzing the results of predictive models. The methods employed are applicable to virtually any predictive model and make comparisons between different methodologies straightforward.",
        "License": "GPL (>= 2)",
        "Depends": "R (>= 2.15.0), xtable, pbapply",
        "Suggests": "randomForest, e1071",
        "NeedsCompilation": "no",
        "Packaged": "2015-08-16 14:17:33 UTC; scott",
        "Repository": "CRAN",
        "Date/Publication": "2015-08-16 23:05:52",
    }


def test_from_file_tar_file_works():
    assert pycran.from_file(tarfile.open(path.join(data_path, "A3_1.0.0.tar.gz"))) == {
        "Package": "A3",
        "Type": "Package",
        "Title": "Accurate, Adaptable, and Accessible Error Metrics for Predictive Models",
        "Version": "1.0.0",
        "Date": "2015-08-15",
        "Author": "Scott Fortmann-Roe",
        "Maintainer": "Scott Fortmann-Roe <scottfr@berkeley.edu>",
        "Description": "Supplies tools for tabulating and analyzing the results of predictive models. The methods employed are applicable to virtually any predictive model and make comparisons between different methodologies straightforward.",
        "License": "GPL (>= 2)",
        "Depends": "R (>= 2.15.0), xtable, pbapply",
        "Suggests": "randomForest, e1071",
        "NeedsCompilation": "no",
        "Packaged": "2015-08-16 14:17:33 UTC; scott",
        "Repository": "CRAN",
        "Date/Publication": "2015-08-16 23:05:52",
    }


def test_from_file_path_raises_exception_if_description_not_found():
    with pytest.raises(DescriptionNotFound):
        pycran.from_file(path.join(data_path, "A3_no_description.tar.gz"))


def test_from_file_tar_file_raises_exception_if_description_not_found():
    with pytest.raises(DescriptionNotFound):
        pycran.from_file(tarfile.open(path.join(data_path, "A3_no_description.tar.gz")))


def test_from_file_path_raises_exception_if_not_exists():
    with pytest.raises(FileNotFoundError):
        pycran.from_file(path.join(data_path, "bobo.tar.gz"))


def test_from_file_path_raises_exception_if_file_is_not_tarfile():
    with pytest.raises(NotTarFile):
        pycran.from_file(path.join(data_path, "PACKAGES_MIX.txt"))
