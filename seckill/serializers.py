from rest_framework import serializers

from seckill.models import Seckill, SuccessKilled


class SeckillSerializer(serializers.ModelSerializer):
     class Meta:
         model=Seckill
         fields=('seckill_id','name','number','start_time','end_time','create_time')


class SuccessKilledSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessKilled
        fields = ('seckill_id', 'user_phone', 'state', 'create_time')

