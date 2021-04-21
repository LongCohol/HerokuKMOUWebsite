import os
from django.core.files.storage import FileSystemStorage


class OverrideExisting(FileSystemStorage):
    """
    FileSystemStorage subclass that allows overwrite the already existing
    files.

    Be careful using this class, as user-uploaded files will overwrite
    already existing files.
    """

    # The combination that don't makes os.open() raise OSError if the
    # file already exists before it's opened.
    OS_OPEN_FLAGS = os.O_WRONLY | os.O_TRUNC | os.O_CREAT | getattr(os, 'O_BINARY', 0)

    def get_available_name(self, name, max_length=None):
        """
        This method will be called before starting the save process.
        """
        return name

