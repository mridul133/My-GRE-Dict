from django.db import models

class Word(models.Model):
    Word = models.CharField(max_length = 25)
    POS = models.CharField(max_length = 20, blank = True)
    Definition = models.CharField(max_length = 100)
    Example = models.TextField(blank = True)
    Weight = models.DecimalField(default = 100, max_digits = 100, decimal_places = 20)
    AppearCnt = models.BigIntegerField(default = 0)
