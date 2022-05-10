# Generated by Django 4.0.4 on 2022-05-05 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0002_delete_purchases'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes', models.CharField(max_length=5)),
                ('amount', models.IntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='connect.articles')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connect.customers_purchase')),
            ],
        ),
    ]
