"""Parse CRAN package metadata"""
from typing import Dict, Generator, Optional, Set

from pycran.util import BytesOrString, PathOrTarFile, as_string, read_description

__version__ = "0.1.1"


def parse(data: BytesOrString) -> Generator:
    """Parses CRAN package metadata from
    https://cran.r-project.org/src/contrib/PACKAGES
    and returns the list of dictionaries.

    Args:
        data (BytesOrString): raw text from the package list

    Returns:
        (Generator): each entry from packages as dictionary
    """
    fields: Set = set()
    package: Dict = {}

    # We want to iterate over each line and accumulate
    # keys in dictionary, once we meet the same key
    # in our dictionary we have a single package
    # metadata parsed so we yield and repeat again.
    for line in data.splitlines():
        line = as_string(line)

        if not line.strip():
            continue

        if ":" in line:
            parts = line.split(":", maxsplit=1)
            field = parts[0].strip()
            value = str("".join(parts[1:]).strip())

            if not field[0].isalpha():
                field = ""
                value = line

            if field and field in fields:
                fields = {field}
                result = {**package}
                package = {field: value}
                if result:
                    yield result
            else:
                # Here we want to parse dangling lines
                # like the ones with long dependency
                # list, `R (>= 2.15.0), xtable, pbapply ... \n    and more`
                package[field] = value
                fields.add(field)
        else:
            pairs = list(package.items())
            if pairs:
                last_field = pairs[-1][0]
                package[last_field] += f" {line.strip()}"

    # We also need to return the metadata for
    # the last parsed package.
    if package:
        yield package


def encode(metadata: Dict) -> Optional[str]:
    """Dump dictionary into the following form

        Package: A3
        Version: 1.0.0
        Depends: R (>= 2.15.0), xtable, pbapply
        Suggests: randomForest, e1071
        License: GPL (>= 2)
        MD5sum: 027ebdd8affce8f0effaecfcd5f5ade2
        NeedsCompilation: no

    Args:
        metadata (Dict): Converts metadata dictionary to deb format

    Returns:
        (Optional[str]): package record as deb format
    """
    return "\n".join([f"{key}: {value}" for key, value in metadata.items()])


def decode(metadata: BytesOrString) -> Optional[Dict]:
    """Parse package metadata
    Note: it is a shorthand to `parse`
          then extracts the first value from it.
    Input should be in the following format
    which is R package metadata description
    see: https://cran.r-project.org/src/contrib/PACKAGES

        Package: A3
        Version: 1.0.0
        Depends: R (>= 2.15.0), xtable, pbapply
        Suggests: randomForest, e1071
        License: GPL (>= 2)
        MD5sum: 027ebdd8affce8f0effaecfcd5f5ade2
        NeedsCompilation: no

    Args:
        metadata (str): metadata text information

    Returns:
        (Optional[Dict]): Parse deb format and return dictionary
    """
    try:
        [package, *_rest] = list(parse(metadata))
        return package
    except (ValueError, TypeError):
        return None


def from_file(archive: PathOrTarFile) -> Optional[Dict]:
    """Load and parse CRAN package archive
    Args:
        archive (PathOrTarFile): path to archive or `tarfile.TarFile` instance

    Returns:
        (dict): Dictionary of R package metadata
    """
    return decode(read_description(archive))
