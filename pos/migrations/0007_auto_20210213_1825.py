# Generated by Django 3.1.6 on 2021-02-13 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_auto_20210212_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopitem',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shopping_products', to='pos.shopping'),
        ),
    ]
