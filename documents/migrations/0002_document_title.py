# Generated by Django 3.0.2 on 2020-02-01 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default=30, max_length=30),
            preserve_default=False,
        ),
    ]
