from django.db import models
from api.models.Vessel import Vessel

class Equipment(models.Model):
    name = models.CharField(null=False, max_length=40)
    code = models.CharField(unique=True, null=False, max_length=40)
    location = models.CharField(null=False, max_length=40)
    status = models.CharField(null=False, max_length=8)
    vessel = models.ForeignKey(Vessel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name