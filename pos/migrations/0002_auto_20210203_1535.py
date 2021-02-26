# Generated by Django 3.1.6 on 2021-02-03 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0002_auto_20210203_1535'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopping',
            name='other_charge_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.chargetype'),
        ),
        migrations.AddField(
            model_name='shopping',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='people.people'),
        ),
        migrations.AddField(
            model_name='shopitem',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product'),
        ),
        migrations.AddField(
            model_name='shopitem',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.shopping'),
        ),
        migrations.AddField(
            model_name='shop',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shops', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymenttype',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.paymenttype'),
        ),
        migrations.AddField(
            model_name='payment',
            name='people',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='people.people'),
        ),
        migrations.AddField(
            model_name='payment',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.shopping'),
        ),
        migrations.AddField(
            model_name='chargetype',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]