from django.db import models


class Vessel(models.Model):
    code = models.CharField(unique=True, null=False, max_length=40)

    def __str__(self):
        return self.code