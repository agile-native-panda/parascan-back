from django.db import models

# Create your models here.

class Media(models.Model):
    #id = models.UUIDField
    video = models.FileField(upload_to="video/")


class Result(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="results")
    #id = models.UUIDField
    content = models.FileField(upload_to="result/")