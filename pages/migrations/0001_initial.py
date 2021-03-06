# Generated by Django 2.0.7 on 2021-05-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Global',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalWords', models.BigIntegerField(default=0)),
                ('MasteredCnt', models.BigIntegerField(default=0)),
                ('AlphaSort', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Word', models.CharField(max_length=25)),
                ('POS', models.CharField(blank=True, max_length=20)),
                ('Definition', models.CharField(max_length=300)),
                ('Example', models.TextField(blank=True)),
                ('Weight', models.FloatField(default=100.0)),
                ('AppearCnt', models.BigIntegerField(default=0)),
            ],
        ),
    ]
