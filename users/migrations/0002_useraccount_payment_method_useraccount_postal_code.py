# Generated by Django 5.0.1 on 2024-05-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('Cash on delivery', 'Cash on delivery'), ('SSLCOMMERZ', 'SSLCOMMERZ')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
