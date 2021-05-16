from django.db import models

class Visitor(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name",'spo2','pulse']

    name=models.CharField(max_length=20)
    spo2=models.IntegerField(default=None)
    pulse=models.IntegerField(default=None)

