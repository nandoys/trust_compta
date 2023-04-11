from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

fs = FileSystemStorage()


def upload_file(file: InMemoryUploadedFile):
    name = fs.save(file.name, file)
    path = fs.path(name)

    return path
