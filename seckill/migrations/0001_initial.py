# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-19 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seckill',
            fields=[
                ('seckill_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('number', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'seckill',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SuccessKilled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seckill_id', models.BigIntegerField()),
                ('user_phone', models.BigIntegerField()),
                ('state', models.IntegerField()),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'success_killed',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='successkilled',
            unique_together=set([('seckill_id', 'user_phone')]),
        ),
    ]
