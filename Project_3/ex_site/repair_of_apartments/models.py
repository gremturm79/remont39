from django.db import models
from main_1.models import PhotoOfWorks, TypeOfServices


class Apartments(models.Model):
    binding = models.ForeignKey(PhotoOfWorks, on_delete=models.CASCADE, null=True, blank=True)


class ApartmentType(models.Model):
    binding = models.ForeignKey(TypeOfServices, on_delete=models.CASCADE, null=True, blank=True)
