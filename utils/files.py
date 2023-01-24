from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile


def upload_file(file: InMemoryUploadedFile):
    fs = FileSystemStorage()
    name = fs.save(file.name, file)
    path = fs.path(name)

    return path
