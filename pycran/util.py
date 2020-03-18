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

        with tarfile.open(archive) as tar:
            description = tar.getmember("DESCRIPTION")
            with tar.fileobject(tar, description) as metadata:
                return as_string(metadata.read())
