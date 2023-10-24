from django.contrib.auth.models import User
from django.db import models
import os


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
    file1 = models.FileField(upload_to=custom_upload_path1, blank=True, null=True)
    file2 = models.FileField(upload_to=custom_upload_path2, blank=True, null=True)
    file3 = models.FileField(upload_to=custom_upload_path3, blank=True, null=True)
    file4 = models.FileField(upload_to=custom_upload_path4, blank=True, null=True)
    file5 = models.FileField(upload_to=custom_upload_path5, blank=True, null=True)
    file1norm = models.FileField(upload_to=custom_upload_path1norm, blank=True, null=True)
    file2norm = models.FileField(upload_to=custom_upload_path2norm, blank=True, null=True)
    file3norm = models.FileField(upload_to=custom_upload_path3norm, blank=True, null=True)
    file4norm = models.FileField(upload_to=custom_upload_path4norm, blank=True, null=True)
    file5norm = models.FileField(upload_to=custom_upload_path5norm, blank=True, null=True)
    order = models.IntegerField(default=0)
