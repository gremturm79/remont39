# Generated by Django 4.1.7 on 2023-06-10 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_1', '0008_remove_myobject_owner_remove_myobject_types_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='image_works/% Y/% m/% d/')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('types', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_1.typeofservices')),
            ],
        ),
    ]