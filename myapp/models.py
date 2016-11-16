from django.db import models

# Create your models here.
NEIGHBORHOOD = (
    ('1', 'Hydepark'),
    ('2', ''),
    ('3', ''),
    ('4', ''),
    ('5', ''),
    ('6', ''),
    ('7', ''),
    ('8', ''),
    ('9', ''),
    ('10', ''),
    .
    .
    .
    .
    ('F', '')
   )

NEIGHBORHOOD_DICT = dict(NEIGHBORHOOD)

class Input(models.Model):

    neighborhood = models.CharField(max_length=2, choices=NEIGHBORHOOD)
    name  = models.CharField(max_length=50)
