# Generated by Django 4.0.4 on 2022-05-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0005_purchases'),
    ]

    operations = [
        migrations.AddField(
            model_name='discounts',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=2),
        ),
    ]