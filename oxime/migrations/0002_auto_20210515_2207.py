# Generated by Django 2.2.7 on 2021-05-15 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxime', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitor',
            options={'ordering': ['name', 'spo2', 'pulse']},
        ),
    ]
