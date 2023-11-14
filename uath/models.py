from django.contrib.auth.models import User
from django.db import models
import os

from django.utils import timezone


def custom_upload_path1(instance, filename):
    new_filename = f"modul1{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path2(instance, filename):
    new_filename = f"modul2{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path3(instance, filename):
    new_filename = f"modul3{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path4(instance, filename):
    new_filename = f"modul4{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path5(instance, filename):
    new_filename = f"modul5{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path1norm(instance, filename):
    new_filename = f"modul1norm{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path2norm(instance, filename):
    new_filename = f"modul2norm{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path3norm(instance, filename):
    new_filename = f"modul3norm{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path4norm(instance, filename):
    new_filename = f"modul4norm{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


def custom_upload_path5norm(instance, filename):
    new_filename = f"modul5norm{os.path.splitext(filename)[1]}"
    return f"{instance.name}/{new_filename}"


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file1 = models.FileField(upload_to=custom_upload_path1)
    file2 = models.FileField(upload_to=custom_upload_path2)
    file3 = models.FileField(upload_to=custom_upload_path3)
    file4 = models.FileField(upload_to=custom_upload_path4)
    file5 = models.FileField(upload_to=custom_upload_path5)
    file1norm = models.FileField(upload_to=custom_upload_path1norm)
    file2norm = models.FileField(upload_to=custom_upload_path2norm)
    file3norm = models.FileField(upload_to=custom_upload_path3norm)
    file4norm = models.FileField(upload_to=custom_upload_path4norm)
    file5norm = models.FileField(upload_to=custom_upload_path5norm)
    order = models.IntegerField(default=0)
    is_dl = models.BooleanField(default=False)
