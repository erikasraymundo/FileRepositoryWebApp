# Generated by Django 4.0.2 on 2022-02-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_management', '0002_category_isarchived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='isArchived',
            field=models.BooleanField(),
        ),
    ]
