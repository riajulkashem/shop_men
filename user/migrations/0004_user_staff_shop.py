# Generated by Django 3.1.6 on 2021-02-05 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_auto_20210203_1535'),
        ('user', '0003_auto_20210205_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='staff_shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='staff_list', to='pos.shop'),
        ),
    ]
