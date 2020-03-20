import tarfile
from os import path
from typing import Union

from pycran.errors import DescriptionNotFound, NotTarFile

PathOrTarFile = Union[tarfile.TarFile, str]
BytesOrString = Union[bytes, str]


def as_string(meta_line: BytesOrString) -> str:
    """Convert bytes to string
    Args:
        meta_line (BytesOrString): raw metadata
    Returns:
        (str): string version of `meta_line`
    """
    if isinstance(meta_line, bytes):
        return meta_line.decode("utf-8")

    return meta_line


def read_description(archive: PathOrTarFile) -> str:
    """Convert bytes to string
    Args:
        archive (PathOrTarFile): path to archive or `TarFile` instance

    Returns:
        (str): contents of description file
    """
    if isinstance(archive, str):
        if not path.exists(archive):
            raise FileNotFoundError(f"File {archive} does not exist.")

        if not tarfile.is_tarfile(archive):
            raise NotTarFile(f"File {archive} is not tar archive.")

        tar: tarfile.TarFile = tarfile.open(archive)
    else:
        tar = archive

    with tar:
        description: tarfile.TarInfo = tar.getmember(get_description_path(tar))
        with tar.fileobject(tar, description) as metadata:  # type: ignore
            return metadata.read()


def get_description_path(tar: tarfile.TarFile) -> str:
    """Lookup description file
    Args:
        tar (tarfile.TarFile): `tarfile.TarFile` instance

    Returns:
        (str): path to description file
    """
    for info in tar.getmembers():
        if "DESCRIPTION" in info.name:
            return info.name

    raise DescriptionNotFound("Description file not found.")
