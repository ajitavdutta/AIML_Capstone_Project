# Generated by Django 4.0 on 2021-12-23 09:28

from django.db import migrations, models
import fileUpload.models


class Migration(migrations.Migration):

    dependencies = [
        ('fileUpload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to=fileUpload.models.generate_filename),
        ),
    ]
