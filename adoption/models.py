from django.contrib.auth.models import User
from django.db import models

from publish.models import Pet


class RequestAdoption(models.Model):
    choices_status = (
        ('WA', 'Waiting for Approval'),
        ('A', 'Approved'),
        ('R', 'Refused'),
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=2, choices=choices_status, default='WA'
        )
     
    def __str__(self):
        return self.pet.name