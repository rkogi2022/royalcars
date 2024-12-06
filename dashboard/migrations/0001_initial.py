# Generated by Django 4.2 on 2024-12-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='car_images/')),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('automation', models.CharField(choices=[('AUTO', 'Automatic'), ('MANUAL', 'Manual')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rental_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passportimage', models.ImageField(blank=True, upload_to='staff_images/')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=100)),
                ('desgination', models.CharField(max_length=100)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('linkedin_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
