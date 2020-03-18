from tarfile import TarError


class DescriptionNotFound(TarError):
    pass


class NotTarFile(TarError):
    pass
