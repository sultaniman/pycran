import os
import tarfile
from typing import Union


PathOrTarFile = Union[tarfile.TarFile, str]
BytesOrString = Union[bytes, str]


def as_string(meta_line: BytesOrString) -> str:
    if isinstance(meta_line, bytes):
        return meta_line.decode("utf-8")

    return meta_line


def get_description(archive: PathOrTarFile) -> str:
    if isinstance(archive, str):
        if not tarfile.is_tarfile(archive):
            raise tarfile.TarError(f"File {archive} is not tar archive")

        filename = os.path.basename(archive)
        [package_name, *_rest] = filename.split("_", maxsplit=1)
        with tarfile.open(archive) as tar:
            description_file = os.path.join(package_name, "DESCRIPTION")
            description = tar.getmember(description_file)
            with tar.fileobject(tar, description) as metadata:
                return as_string(metadata.read())
