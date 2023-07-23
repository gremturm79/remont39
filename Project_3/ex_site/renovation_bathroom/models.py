from django.db import models
from main_1.models import TypeOfServices, PhotoOfWorks


class BathRoom(models.Model):
    binding = models.ForeignKey(PhotoOfWorks, on_delete=models.CASCADE, null=True, blank=True)


class BathRoomType(models.Model):
    binding = models.ForeignKey(TypeOfServices, on_delete=models.CASCADE, null=True, blank=True)


