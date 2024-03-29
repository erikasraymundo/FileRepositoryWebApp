# Generated by Django 4.0 on 2022-02-12 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_management', '0001_initial'),
        ('category_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_management.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.user')),
            ],
        ),
    ]
