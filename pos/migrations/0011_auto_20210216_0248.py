# Generated by Django 3.1.6 on 2021-02-16 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0010_auto_20210215_1910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='shop',
            new_name='Shopping',
        ),
        migrations.RenameField(
            model_name='shopping',
            old_name='total',
            new_name='charge_total',
        ),
        migrations.AddField(
            model_name='shopping',
            name='discount_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopping',
            name='grand_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopping',
            name='sub_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='reference',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
