# Generated by Django 5.0.1 on 2024-05-01 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='fruit',
            new_name='item',
        ),
    ]
