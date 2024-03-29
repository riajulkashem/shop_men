# Generated by Django 3.1.6 on 2021-02-18 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0013_shop_address'),
        ('people', '0003_auto_20210208_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='people', to='pos.shop'),
        ),
    ]
