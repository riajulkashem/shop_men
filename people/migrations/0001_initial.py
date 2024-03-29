# Generated by Django 3.1.6 on 2021-02-03 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Phone Number', regex='^(?:\\+8801|01)?(\\d{9})$'), django.core.validators.MinLengthValidator(limit_value=11)])),
                ('people_type', models.CharField(choices=[('customer', 'Customer'), ('supplier', 'Supplier')], max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='people/photo/')),
                ('address', models.TextField()),
                ('opening_balance', models.IntegerField(default=0)),
                ('due', models.IntegerField(default=0)),
                ('return_due', models.IntegerField(default=0)),
                ('total_paid', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
