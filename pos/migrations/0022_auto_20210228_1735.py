# Generated by Django 3.1.7 on 2021-02-28 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210208_1552'),
        ('pos', '0021_auto_20210226_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='capital',
            field=models.IntegerField(default=0, help_text='current cash which will be counted as cash amount', verbose_name='Opening Balance'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shoppings', to='product.product'),
        ),
    ]