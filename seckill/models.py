# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Seckill(models.Model):
    seckill_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'seckill'



class SuccessKilled(models.Model):
    seckill_id = models.BigIntegerField()
    user_phone = models.BigIntegerField()
    state = models.IntegerField()
    create_time = models.DateTimeField()

    def __unicode__(self):
        return '%s,%s'%(self.seckill_id,self.user_phone)

    class Meta:
        managed = True
        db_table = 'success_killed'
        unique_together = (('seckill_id', 'user_phone'),)