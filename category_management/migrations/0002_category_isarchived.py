# Generated by Django 4.0.2 on 2022-02-13 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='isArchived',
            field=models.BooleanField(default=False, verbose_name=False),
            preserve_default=False,
        ),
    ]
