# Generated by Django 4.0.2 on 2022-02-16 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default=None, max_length=254, null=True, upload_to='profile_pics/'),
        ),
    ]
