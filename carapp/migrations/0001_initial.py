# Generated by Django 4.2 on 2024-12-06 08:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('county', models.CharField(max_length=100)),
                ('driving_class', models.CharField(choices=[('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Pass', 'Pass'), ('Fail', 'Fail')], default='pending', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RideHailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('pickup_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('pickup_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('dropoff_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('dropoff_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.TimeField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('id_number', models.CharField(max_length=20)),
                ('kra_pin', models.CharField(max_length=20)),
                ('road_test_date', models.DateField()),
                ('road_test_confirmed', models.BooleanField(default=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='dashboard.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('phone_number', models.CharField(default=None, max_length=15)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=datetime.date.today)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deposit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('transaction_time', models.DateTimeField(blank=True, null=True)),
                ('car', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.car')),
            ],
        ),
    ]