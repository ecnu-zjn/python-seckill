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
    id = models.BigIntegerField(primary_key=True)
    seckill_id = models.BigIntegerField()
    user_phone = models.BigIntegerField()
    state = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'success_killed'

class Exposed(object):
    def __init__(self,exposed,seckill_id):
        self.exposed = exposed
        self.seckill_id = seckill_id

class ExposedNoId(Exposed):
    def __init__(self,exposed,seckill_id):
        Exposed.__init__(self,exposed,seckill_id)

class ExposedNoOpen(Exposed):
    def __init__(self,exposed,seckill_id,now,start,end):
        Exposed.__init__(self,exposed,seckill_id)
        self.now=now
        self.start=start
        self.end=end

class ExposedOpen(Exposed):
    def __init__(self,exposed,seckill_id,md5):
        Exposed.__init__(self,exposed,seckill_id)
        self.md5=md5


