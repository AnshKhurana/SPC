# Generated by Django 2.1.1 on 2018-10-24 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filedatabase', '0014_auto_20181024_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filerecord',
            name='file_data',
            field=models.TextField(default=b''),
        ),
    ]