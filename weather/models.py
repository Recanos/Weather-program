# models.py
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} | {self.id}'