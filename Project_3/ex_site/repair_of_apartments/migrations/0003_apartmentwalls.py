# Generated by Django 4.1.7 on 2023-05-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_of_apartments', '0002_apartmentdismantling_apartmentpricing'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentWalls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]