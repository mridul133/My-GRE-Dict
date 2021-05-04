from django.db import models

class Word(models.Model):
    Word = models.CharField(max_length = 25)
    POS = models.CharField(max_length = 20, blank = True)
    Definition = models.CharField(max_length = 300)
    Example = models.TextField(blank = True)
    Weight = models.FloatField(default = 100.0)
    AppearCnt = models.BigIntegerField(default = 0)
    IsCached = models.BigIntegerField(default = 0)


class Global(models.Model):
    TotalWords = models.BigIntegerField(default = 0)
    MasteredCnt = models.BigIntegerField(default = 0)
    AlphaSort = models.BigIntegerField(default = 0)
    ShowFromCache = models.BigIntegerField(default = 0)