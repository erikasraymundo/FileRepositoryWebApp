# Generated by Django 4.0.2 on 2022-02-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_management', '0004_alter_category_isarchived'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(default='admin', max_length=100)),
            ],
        ),
    ]