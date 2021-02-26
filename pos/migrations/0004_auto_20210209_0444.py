# Generated by Django 3.1.6 on 2021-02-09 04:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_auto_20210208_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitem',
            name='total',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='shopping',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 4, 44, 34, 535240, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopping',
            name='reference',
            field=models.CharField(default='OK', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shopping_products', to='pos.tax'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='tax_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shopping_products', to='pos.chargetype'),
        ),
    ]